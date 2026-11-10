import pandas as pd
import geopandas as gpd
from rasterstats import zonal_stats
import os
import geobr
import numpy as np
import rasterio

def processar_dados_soilgrids(pasta_rasters: str) -> pd.DataFrame:
    """Processa múltiplos rasters do SoilGrids e extrai a média por microrregião."""
    
    print("Carregando mapa de microrregiões do geobr...")
    gdf_micro = geobr.read_micro_region(year=2020)
    
    # Inicia o DataFrame com a chave padronizada (só com os códigos únicos)
    df_solo = pd.DataFrame({'CD_MICRO': gdf_micro['code_micro'].astype(int).astype(str)})
    
    # Lista todos os arquivos .tif na pasta
    arquivos_raster = [f for f in os.listdir(pasta_rasters) if f.endswith('.tif')]
    print(f"Encontrados {len(arquivos_raster)} arquivos raster para processar.")
    
    for i, raster in enumerate(arquivos_raster):
        nome_variavel = raster.replace('.tif', '') # Ex: 'phh2o_0-5cm_mean'
        caminho_completo = os.path.join(pasta_rasters, raster)
        
        print(f"  [{i+1}/{len(arquivos_raster)}] Extraindo {nome_variavel}...")
        
        try:
            # 1. Lê o CRS e o valor de Nodata direto do arquivo .tif
            with rasterio.open(caminho_completo) as src:
                crs_raster = src.crs
                nodata_val = src.nodata if src.nodata is not None else -32768.0
            
            # 2. Reprojetar o shapefile do geobr para o mesmo CRS do raster
            gdf_micro_proj = gdf_micro.to_crs(crs_raster)
            
            # 3. Calcular as estatísticas zonais
            stats = zonal_stats(
                gdf_micro_proj, 
                caminho_completo, 
                stats=['mean'], 
                nodata=nodata_val
            )
            
            # 4. Extrair valores numéricos
            valores = [s['mean'] for s in stats]
            df_solo[nome_variavel] = valores
            
        except Exception as e:
            print(f"     ⚠️ Erro ao processar {raster}: {e}")
            df_solo[nome_variavel] = np.nan
            
    return df_solo
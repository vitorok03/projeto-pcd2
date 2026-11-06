import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import os
import numpy as np
import geobr
import zipfile
import io

def carregar_e_agregar_inmet(pasta_zip: str) -> pd.DataFrame:
    """Lê os arquivos ZIP do INMET, calcula métricas agronômicas e agrega para DIÁRIO."""
    dfs_diarios = []
    print(f"Verificando arquivos na pasta: {pasta_zip}")
    
    arquivos_zip = [f for f in os.listdir(pasta_zip) if f.lower().endswith('.zip')]
    if not arquivos_zip:
         raise ValueError(f"Nenhum arquivo .zip encontrado na pasta {pasta_zip}")

    for arquivo in arquivos_zip:
        caminho_zip = os.path.join(pasta_zip, arquivo)
        try:
            with zipfile.ZipFile(caminho_zip, 'r') as z:
                arquivos_internos = [n for n in z.namelist() if n.lower().endswith(('.csv', '.txt'))]
                
                for nome_csv in arquivos_internos:
                    with z.open(nome_csv) as f:
                        bytes_content = f.read()
                        try:
                            conteudo = bytes_content.decode('utf-8-sig').splitlines()
                        except UnicodeDecodeError:
                            conteudo = bytes_content.decode('latin1').splitlines()
                        
                        codigo, lat, lon, uf, estacao = None, None, None, None, None
                        header_idx = -1
                        
                        # Varre as primeiras 15 linhas
                        for i, line in enumerate(conteudo[:15]):
                            if 'CODIGO (WMO)' in line.upper():
                                codigo = line.split(';')[1].strip()
                            elif 'LATITUDE' in line.upper():
                                lat = float(line.split(';')[1].strip().replace(',', '.'))
                            elif 'LONGITUDE' in line.upper():
                                lon = float(line.split(';')[1].strip().replace(',', '.'))
                            elif 'UF:' in line.upper():
                                uf = line.split(';')[1].strip()
                            elif 'ESTACAO:' in line.upper() or 'ESTAÇÃO:' in line.upper():
                                estacao = line.split(';')[1].strip()
                            elif 'DATA' in line.upper() and 'HORA' in line.upper():
                                header_idx = i
                                break
                        
                        if not (codigo and lat and lon and header_idx != -1):
                            continue
                            
                        dados_texto = "\n".join(conteudo[header_idx:])
                        df = pd.read_csv(io.StringIO(dados_texto), sep=';', encoding='latin1')
                        
                        # --- MAPEAMENTO TOLERANTE DE COLUNAS ---
                        def achar_coluna(termo):
                            for c in df.columns:
                                if termo.lower() in c.lower(): return c
                            return None

                        col_data = achar_coluna('DATA')
                        col_prec = achar_coluna('PRECIPITA')
                        col_temp = achar_coluna('BULBO SECO')
                        col_umid = achar_coluna('UMIDADE')
                        col_rad = achar_coluna('RADIACAO')
                        col_vento = achar_coluna('VENTO')

                        if not (col_data and col_prec and col_temp):
                            continue

                        # Renomeia para padronizar
                        df = df.rename(columns={
                            col_data: 'data', col_prec: 'prec_total', col_temp: 'temp_media',
                            col_umid: 'umid_media', col_rad: 'radiacao_total', col_vento: 'vento_medio'
                        })
                        
                        # Converte para numérico (lidando com vírgulas)
                        df['data'] = pd.to_datetime(df['data'], errors='coerce')
                        for c in ['prec_total', 'temp_media', 'umid_media', 'radiacao_total', 'vento_medio']:
                            if c in df.columns:
                                df[c] = pd.to_numeric(df[c].astype(str).str.replace(',', '.'), errors='coerce')
                            else:
                                df[c] = np.nan

                        df = df.dropna(subset=['data']).replace(-9999, np.nan)
                        
                        # --- AGREGAÇÃO DIÁRIA ---
                        # AQUI ESTÁ A CORREÇÃO: temp_max e temp_min são calculados a partir da coluna horária
                        agg_dict = {
                            'prec_total': 'sum',
                            'temp_media': 'mean',
                            'umid_media': 'mean',
                            'radiacao_total': 'sum',
                            'vento_medio': 'mean',
                        }
                        agg_dict = {k: v for k, v in agg_dict.items() if k in df.columns}
                        
                        df_diario = df.groupby('data').agg(agg_dict).reset_index()
                        
                        # Calcula max/min a partir das leituras horárias
                        df_diario['temp_max'] = df.groupby('data')['temp_media'].max().values
                        df_diario['temp_min'] = df.groupby('data')['temp_media'].min().values
                        df_diario['n_horas_validas'] = df.groupby('data')['temp_media'].count().values
                        
                        # FILTRO: Mantém apenas dias com pelo menos 18 horas válidas (igual ao código antigo)
                        df_diario = df_diario[df_diario['n_horas_validas'] >= 18].copy()
                        
                        if df_diario.empty:
                            continue

                        # 1. Amplitude Térmica
                        df_diario['amplitude_termica'] = df_diario['temp_max'] - df_diario['temp_min']
                            
                        # 2. Dia Seco (padrão agronômico: < 2mm de chuva)
                        df_diario['dia_seco'] = (df_diario['prec_total'] < 2.0).astype(int)
                        
                        # 3. GDD (Graus-Dia de Crescimento) - Base 10°C para soja
                        df_diario['gdd'] = (((df_diario['temp_max'] + df_diario['temp_min']) / 2) - 10).clip(lower=0)
                        
                        # Informações da estação
                        df_diario['codigo_estacao'] = codigo
                        df_diario['VL_LATITUDE'] = lat
                        df_diario['VL_LONGITUDE'] = lon
                        df_diario['uf'] = uf
                        df_diario['estacao'] = estacao
                        
                        dfs_diarios.append(df_diario)
                            
        except Exception as e:
            print(f"Erro ao processar {arquivo}: {e}")

    if not dfs_diarios:
        raise ValueError("Nenhum arquivo de dados válido foi processado.")
    
    df_final = pd.concat(dfs_diarios, ignore_index=True)
    # REMOVE DUPLICATAS: Se a mesma estação tiver o mesmo dia em dois arquivos CSV, mantém apenas 1
    df_final = df_final.drop_duplicates(subset=['codigo_estacao', 'data'], keep='first')
    df_final['ano'] = df_final['data'].dt.year
    df_final['mes'] = df_final['data'].dt.month
    df_final = df_final[df_final['ano'] >= 2005].copy() #igual ao .parquet og
    return df_final

def realizar_join_espacial_estacoes(df_clima_diario: pd.DataFrame) -> pd.DataFrame:
    df_estacoes = df_clima_diario[['codigo_estacao', 'VL_LATITUDE', 'VL_LONGITUDE']].drop_duplicates()
    geometria = [Point(xy) for xy in zip(df_estacoes['VL_LONGITUDE'], df_estacoes['VL_LATITUDE'])]
    gdf_estacoes = gpd.GeoDataFrame(df_estacoes, geometry=geometria, crs="EPSG:4326")
    
    gdf_micro = geobr.read_micro_region(year=2020)
    gdf_micro = gdf_micro.to_crs("EPSG:4326")
        
    gdf_join = gpd.sjoin(gdf_estacoes, gdf_micro, how="inner", predicate="intersects")
    return pd.DataFrame(gdf_join.drop(columns='geometry'))

# No topo do arquivo, adicione o import:
from .geo import construir_mapa_estacao_microrregiao

def processar_dados_inmet(caminho_pasta_dados: str) -> tuple:
    """Pipeline completo de clima: lê, agrega e faz o join espacial com fallback."""
    print("Lendo e agregando arquivos ZIP do INMET (Otimizado)...")
    df_diario = carregar_e_agregar_inmet(caminho_pasta_dados)
    
    print("Gerando mapa espacial (Estação -> Microrregião) com fallback...")
    df_mapa = construir_mapa_estacao_microrregiao(df_diario)
    df_mapa = df_mapa.rename(columns={'code_micro': 'CD_MICRO', 'name_micro': 'NM_MICRO'})
    
    # O clima diário não precisa mais das colunas de microrregião (elas ficam no mapa)
    # Se a função carregar_e_agregar_inmet já criou essas colunas, a gente remove:
    for col in ['CD_MICRO', 'NM_MICRO']:
        if col in df_diario.columns:
            df_diario = df_diario.drop(columns=[col])
            
    return df_diario, df_mapa
"""Join espacial entre estações meteorológicas e microrregiões com fallbacks."""
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

DISTANCIA_MAXIMA_KM = 150

def montar_geodataframe_estacoes(df_clima_diario):
    """Extrai estações únicas (com coordenadas) do clima diário."""
    estacoes = df_clima_diario[['codigo_estacao', 'VL_LATITUDE', 'VL_LONGITUDE']].drop_duplicates()
    geometria = [Point(lon, lat) for lon, lat in zip(estacoes['VL_LONGITUDE'], estacoes['VL_LATITUDE'])]
    return gpd.GeoDataFrame(estacoes, geometry=geometria, crs="EPSG:4326")

def construir_mapa_estacao_microrregiao(df_clima_diario, distancia_maxima_km=DISTANCIA_MAXIMA_KM):
    """Pipeline completo: estações -> microrregiões com dois fallbacks."""
    import geobr
    microrregioes = geobr.read_micro_region(year=2020).to_crs(epsg=4326)
    microrregioes['code_micro'] = microrregioes['code_micro'].astype(int).astype(str)

    estacoes_geo = montar_geodataframe_estacoes(df_clima_diario).to_crs(microrregioes.crs)

    estacoes_com_micro = gpd.sjoin(
        estacoes_geo,
        microrregioes[['code_micro', 'name_micro', 'geometry']],
        how='left',
        predicate='within',
    )

    # --- Fallback 1: estação fora de qualquer polígono ---
    sem_correspondencia = estacoes_com_micro[estacoes_com_micro['code_micro'].isna()].copy()
    if len(sem_correspondencia) > 0:
        microrregioes_m = microrregioes.to_crs(epsg=5880)
        sem_m = sem_correspondencia[['codigo_estacao', 'geometry']].to_crs(epsg=5880)
        mais_proximo = gpd.sjoin_nearest(
            sem_m, microrregioes_m[['code_micro', 'name_micro', 'geometry']],
            how='left', distance_col='distancia_m',
        )
        mais_proximo['distancia_km'] = mais_proximo['distancia_m'] / 1000
        dentro = mais_proximo[mais_proximo['distancia_km'] <= distancia_maxima_km]
        excluidas = mais_proximo[mais_proximo['distancia_km'] > distancia_maxima_km]
        if len(excluidas) > 0:
            print(f"  {len(excluidas)} estação(ões) excluída(s) por estarem a mais de {distancia_maxima_km}km.")

        subs = (dentro[['codigo_estacao', 'code_micro', 'name_micro']]
                .drop_duplicates('codigo_estacao')
                .rename(columns={'code_micro': 'code_micro_sub', 'name_micro': 'name_micro_sub'}))
        estacoes_com_micro = estacoes_com_micro.merge(subs, on='codigo_estacao', how='left')
        estacoes_com_micro['code_micro'] = estacoes_com_micro['code_micro'].fillna(estacoes_com_micro['code_micro_sub'])
        estacoes_com_micro['name_micro'] = estacoes_com_micro['name_micro'].fillna(estacoes_com_micro['name_micro_sub'])
        estacoes_com_micro = estacoes_com_micro.drop(columns=['code_micro_sub', 'name_micro_sub'])

    estacoes_com_micro = estacoes_com_micro.assign(origem='dentro_do_poligono').copy()

    # --- Fallback 2: microrregião sem NENHUMA estação ---
    micro_com_estacao = set(estacoes_com_micro['code_micro'].dropna())
    todas_micro = set(microrregioes['code_micro'])
    micro_vazias = todas_micro - micro_com_estacao
    print(f"  {len(micro_vazias)} de {len(todas_micro)} microrregiões sem estação dentro. Aplicando fallback 2...")

    if micro_vazias:
        micro_v = microrregioes[microrregioes['code_micro'].isin(micro_vazias)].copy()
        micro_v_m = micro_v.to_crs(epsg=5880)
        micro_v_m['geometry'] = micro_v_m.geometry.centroid

        estacoes_m = estacoes_geo.to_crs(epsg=5880)
        substituta = gpd.sjoin_nearest(
            micro_v_m[['code_micro', 'name_micro', 'geometry']],
            estacoes_m[['codigo_estacao', 'geometry']],
            how='left', distance_col='distancia_m',
        )
        substituta['distancia_km'] = substituta['distancia_m'] / 1000
        longe = substituta[substituta['distancia_km'] > distancia_maxima_km]
        if len(longe) > 0:
            print(f"  {len(longe)} microrregião(ões) sem substituta dentro de {distancia_maxima_km}km.")
        substituta = substituta[substituta['distancia_km'] <= distancia_maxima_km]

        orfas = substituta[['code_micro', 'name_micro', 'codigo_estacao']].assign(origem='substituta_por_centroide')
        estacoes_com_micro = pd.concat([estacoes_com_micro, orfas], ignore_index=True)

    return estacoes_com_micro[['codigo_estacao', 'code_micro', 'name_micro', 'origem']]

def refazer_join_no_parquet(caminho_clima_parquet, caminho_saida):
    """Refaz o join em cima do parquet já processado (sem reprocessar ZIPs)."""
    print("Carregando clima_diario.parquet...")
    df_clima = pd.read_parquet(caminho_clima_parquet)
    print(f"  {len(df_clima)} linhas, {df_clima['CD_MICRO'].nunique() if 'CD_MICRO' in df_clima.columns else 0} microrregiões cobertas antes.")

    # Remove as colunas antigas de microrregião
    for c in ['CD_MICRO', 'NM_MICRO']:
        if c in df_clima.columns:
            df_clima = df_clima.drop(columns=[c])

    print("Aplicando join espacial com fallbacks...")
    mapa = construir_mapa_estacao_microrregiao(df_clima)

    df_clima_novo = df_clima.merge(mapa, on='codigo_estacao', how='left')
    df_clima_novo = df_clima_novo.rename(columns={'code_micro': 'CD_MICRO', 'name_micro': 'NM_MICRO'})

    print(f"  {df_clima_novo['CD_MICRO'].nunique()} microrregiões cobertas após o fallback.")
    df_clima_novo.to_parquet(caminho_saida, index=False)
    print(f"✅ Salvo em {caminho_saida}")

    return df_clima_novo
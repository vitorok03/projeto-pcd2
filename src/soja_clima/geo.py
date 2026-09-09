"""Join espacial entre estações meteorológicas (pontos) e microrregiões
(polígonos do geobr). Requer geopandas e shapely -- não disponíveis no
ambiente de teste usado para validar o resto do pacote, então valide os
resultados intermediários (prints) ao rodar isso pela primeira vez."""
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

DISTANCIA_MAXIMA_KM = 150  # acima disso, não faz sentido físico atribuir


def montar_geodataframe_estacoes(diario):
    """Extrai as estações únicas do diário e resolve coordenadas
    divergentes entre arquivos de anos diferentes (deriva de metadado no
    cabeçalho do INMET), usando a mediana."""
    estacoes = diario[['codigo_estacao', 'estacao', 'uf', 'latitude', 'longitude']].drop_duplicates()

    duplicadas = estacoes[estacoes.duplicated('codigo_estacao', keep=False)]
    if len(duplicadas) > 0:
        print(f"{duplicadas['codigo_estacao'].nunique()} estação(ões) com coordenadas "
              "divergentes entre arquivos -- usando a mediana das coordenadas.")

    estacoes = (estacoes.groupby('codigo_estacao', as_index=False)
                .agg(estacao=('estacao', 'first'), uf=('uf', 'first'),
                     latitude=('latitude', 'median'), longitude=('longitude', 'median')))

    geometria = [Point(lon, lat) for lon, lat in zip(estacoes['longitude'], estacoes['latitude'])]
    return gpd.GeoDataFrame(estacoes, geometry=geometria, crs="EPSG:4326")


def construir_mapa_estacao_microrregiao(diario, microrregioes, distancia_maxima_km=DISTANCIA_MAXIMA_KM):
    """Pipeline completo: estações -> microrregiões, com os dois
    fallbacks (estação fora de qualquer polígono, e microrregião sem
    nenhuma estação dentro), respeitando um limiar de distância máxima
    para não forçar atribuições sem sentido físico (ex: estação
    antártica, arquipélagos oceânicos)."""
    estacoes_geo = montar_geodataframe_estacoes(diario).to_crs(microrregioes.crs)

    estacoes_com_micro = gpd.sjoin(
        estacoes_geo,
        microrregioes[['code_micro', 'name_micro', 'geometry']],
        how='left',
        predicate='within',
    )

    # --- Fallback 1: estação que não caiu em nenhum polígono ---
    sem_correspondencia = estacoes_com_micro[estacoes_com_micro['code_micro'].isna()].copy()
    if len(sem_correspondencia) > 0:
        microrregioes_m = microrregioes.to_crs(epsg=5880)
        sem_correspondencia_m = sem_correspondencia[['codigo_estacao', 'geometry']].to_crs(epsg=5880)

        mais_proximo = gpd.sjoin_nearest(
            sem_correspondencia_m,
            microrregioes_m[['code_micro', 'name_micro', 'geometry']],
            how='left', distance_col='distancia_m',
        )
        mais_proximo['distancia_km'] = mais_proximo['distancia_m'] / 1000

        dentro_do_limiar = mais_proximo[mais_proximo['distancia_km'] <= distancia_maxima_km]
        excluidas = mais_proximo[mais_proximo['distancia_km'] > distancia_maxima_km]
        if len(excluidas) > 0:
            print(f"{len(excluidas)} estação(ões) excluída(s) por estarem a mais de "
                  f"{distancia_maxima_km}km de qualquer microrregião.")

        substituicoes = (dentro_do_limiar[['codigo_estacao', 'code_micro', 'name_micro']]
                          .drop_duplicates('codigo_estacao')
                          .rename(columns={'code_micro': 'code_micro_sub', 'name_micro': 'name_micro_sub'}))
        estacoes_com_micro = estacoes_com_micro.merge(substituicoes, on='codigo_estacao', how='left')
        estacoes_com_micro['code_micro'] = estacoes_com_micro['code_micro'].fillna(estacoes_com_micro['code_micro_sub'])
        estacoes_com_micro['name_micro'] = estacoes_com_micro['name_micro'].fillna(estacoes_com_micro['name_micro_sub'])
        estacoes_com_micro = estacoes_com_micro.drop(columns=['code_micro_sub', 'name_micro_sub'])

    estacoes_com_micro = estacoes_com_micro.assign(origem='dentro_do_poligono').copy()

    # --- Fallback 2: microrregião sem NENHUMA estação dentro ---
    microrregioes_com_estacao = set(estacoes_com_micro['code_micro'].dropna())
    todas_microrregioes = set(microrregioes['code_micro'])
    microrregioes_vazias = todas_microrregioes - microrregioes_com_estacao
    print(f"{len(microrregioes_vazias)} de {len(todas_microrregioes)} microrregiões "
          "não têm nenhuma estação dentro delas.")

    if microrregioes_vazias:
        micro_vazias = microrregioes[microrregioes['code_micro'].isin(microrregioes_vazias)].copy()
        micro_vazias_m = micro_vazias.to_crs(epsg=5880)
        micro_vazias_m['geometry'] = micro_vazias_m.centroid

        estacoes_m = estacoes_geo.to_crs(epsg=5880)
        substituta = gpd.sjoin_nearest(
            micro_vazias_m[['code_micro', 'name_micro', 'geometry']],
            estacoes_m[['codigo_estacao', 'estacao', 'geometry']],
            how='left', distance_col='distancia_m',
        )
        substituta['distancia_km'] = substituta['distancia_m'] / 1000

        longe_demais = substituta[substituta['distancia_km'] > distancia_maxima_km]
        if len(longe_demais) > 0:
            print(f"{len(longe_demais)} microrregião(ões) sem substituta dentro de "
                  f"{distancia_maxima_km}km -- ficarão sem clima.")
        substituta = substituta[substituta['distancia_km'] <= distancia_maxima_km]

        orfas = substituta[['code_micro', 'name_micro', 'codigo_estacao']].assign(origem='substituta_por_centroide')
        estacoes_com_micro = pd.concat([estacoes_com_micro, orfas], ignore_index=True)

    return estacoes_com_micro[['codigo_estacao', 'estacao', 'uf', 'code_micro', 'name_micro', 'origem']]

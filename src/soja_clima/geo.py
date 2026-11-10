"""Join espacial entre estações meteorológicas (pontos) e microrregiões
(polígonos do geobr), com fallbacks. Requer geopandas e shapely -- não
disponíveis no ambiente de teste usado para validar o resto do pacote,
então valide os resultados intermediários (prints) ao rodar isso pela
primeira vez.

Aceita tanto o diário da main (colunas `latitude`/`longitude`, vindo de
`inmet.ler_e_agregar_diario`) quanto o diário da refatoração (colunas
`VL_LATITUDE`/`VL_LONGITUDE`, vindo de `clima.carregar_e_agregar_inmet`).
"""
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

DISTANCIA_MAXIMA_KM = 150  # acima disso, não faz sentido físico atribuir

# (nome canônico, alternativas aceitas) para as coordenadas
_COLUNAS_COORD = {
    'latitude': ('latitude', 'VL_LATITUDE'),
    'longitude': ('longitude', 'VL_LONGITUDE'),
}


def _achar_coluna(df, alternativas):
    for c in alternativas:
        if c in df.columns:
            return c
    raise KeyError(f"Nenhuma das colunas {alternativas} encontrada no diário.")


def carregar_microrregioes(ano=2020):
    """Carrega os polígonos de microrregiões do geobr em EPSG:4326, com
    `code_micro` padronizado como string sem '.0'."""
    import geobr
    microrregioes = geobr.read_micro_region(year=ano).to_crs(epsg=4326)
    microrregioes['code_micro'] = microrregioes['code_micro'].astype(int).astype(str)
    return microrregioes


def montar_geodataframe_estacoes(diario):
    """Extrai as estações únicas do diário e resolve coordenadas
    divergentes entre arquivos de anos diferentes (deriva de metadado no
    cabeçalho do INMET), usando a mediana."""
    col_lat = _achar_coluna(diario, _COLUNAS_COORD['latitude'])
    col_lon = _achar_coluna(diario, _COLUNAS_COORD['longitude'])
    extras = [c for c in ('estacao', 'uf') if c in diario.columns]

    estacoes = (diario[['codigo_estacao', *extras, col_lat, col_lon]]
                .drop_duplicates()
                .rename(columns={col_lat: 'latitude', col_lon: 'longitude'}))

    duplicadas = estacoes[estacoes.duplicated('codigo_estacao', keep=False)]
    if len(duplicadas) > 0:
        print(f"{duplicadas['codigo_estacao'].nunique()} estação(ões) com coordenadas "
              "divergentes entre arquivos -- usando a mediana das coordenadas.")

    agregacoes = {c: (c, 'first') for c in extras}
    estacoes = (estacoes.groupby('codigo_estacao', as_index=False)
                .agg(**agregacoes, latitude=('latitude', 'median'), longitude=('longitude', 'median')))
    for c in ('estacao', 'uf'):
        if c not in estacoes.columns:
            estacoes[c] = pd.NA

    geometria = [Point(lon, lat) for lon, lat in zip(estacoes['longitude'], estacoes['latitude'])]
    return gpd.GeoDataFrame(estacoes, geometry=geometria, crs="EPSG:4326")


def construir_mapa_estacao_microrregiao(diario, microrregioes=None, distancia_maxima_km=DISTANCIA_MAXIMA_KM):
    """Pipeline completo: estações -> microrregiões, com os dois
    fallbacks (estação fora de qualquer polígono, e microrregião sem
    nenhuma estação dentro), respeitando um limiar de distância máxima
    para não forçar atribuições sem sentido físico (ex: estação
    antártica, arquipélagos oceânicos).

    `microrregioes` é opcional: se não for passado, os polígonos são
    carregados do geobr (2020) via `carregar_microrregioes`."""
    if microrregioes is None:
        microrregioes = carregar_microrregioes()

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
        micro_vazias_m['geometry'] = micro_vazias_m.geometry.centroid

        estacoes_m = estacoes_geo.to_crs(epsg=5880)
        substituta = gpd.sjoin_nearest(
            micro_vazias_m[['code_micro', 'name_micro', 'geometry']],
            estacoes_m[['codigo_estacao', 'estacao', 'uf', 'geometry']],
            how='left', distance_col='distancia_m',
        )
        substituta['distancia_km'] = substituta['distancia_m'] / 1000

        longe_demais = substituta[substituta['distancia_km'] > distancia_maxima_km]
        if len(longe_demais) > 0:
            print(f"{len(longe_demais)} microrregião(ões) sem substituta dentro de "
                  f"{distancia_maxima_km}km -- ficarão sem clima.")
        substituta = substituta[substituta['distancia_km'] <= distancia_maxima_km]

        orfas = (substituta[['code_micro', 'name_micro', 'codigo_estacao', 'estacao', 'uf']]
                 .assign(origem='substituta_por_centroide'))
        estacoes_com_micro = pd.concat([estacoes_com_micro, orfas], ignore_index=True)

    return estacoes_com_micro[['codigo_estacao', 'estacao', 'uf', 'code_micro', 'name_micro', 'origem']]


def refazer_join_no_parquet(caminho_clima_parquet, caminho_saida, microrregioes=None):
    """Refaz o join em cima do parquet já processado (sem reprocessar ZIPs)."""
    print("Carregando clima_diario.parquet...")
    df_clima = pd.read_parquet(caminho_clima_parquet)
    print(f"  {len(df_clima)} linhas, {df_clima['CD_MICRO'].nunique() if 'CD_MICRO' in df_clima.columns else 0} microrregiões cobertas antes.")

    # Remove as colunas antigas de microrregião
    for c in ['CD_MICRO', 'NM_MICRO']:
        if c in df_clima.columns:
            df_clima = df_clima.drop(columns=[c])

    print("Aplicando join espacial com fallbacks...")
    mapa = construir_mapa_estacao_microrregiao(df_clima, microrregioes)
    # estacao/uf já existem no diário; o mapa só precisa trazer a microrregião
    mapa = mapa[['codigo_estacao', 'code_micro', 'name_micro', 'origem']]

    df_clima_novo = df_clima.merge(mapa, on='codigo_estacao', how='left')
    df_clima_novo = df_clima_novo.rename(columns={'code_micro': 'CD_MICRO', 'name_micro': 'NM_MICRO'})

    print(f"  {df_clima_novo['CD_MICRO'].nunique()} microrregiões cobertas após o fallback.")
    df_clima_novo.to_parquet(caminho_saida, index=False)
    print(f"✅ Salvo em {caminho_saida}")

    return df_clima_novo


_CACHE_MAPA = {}


def mapa_estacoes_cd_micro(clima_diario):
    """Mapa estação -> microrregião gerado EM MEMÓRIA (o mesmo do main.ipynb),
    com as colunas `codigo_estacao`, `CD_MICRO`, `NM_MICRO` e `origem`.
    Aceita o DataFrame do diário ou o caminho do `clima_diario.parquet`
    (nesse caso o resultado fica em cache durante a sessão)."""
    chave = str(clima_diario) if not isinstance(clima_diario, pd.DataFrame) else None
    if chave in _CACHE_MAPA:
        return _CACHE_MAPA[chave].copy()
    if chave is not None:
        colunas = pd.read_parquet(clima_diario, columns=None).columns
        usar = [c for c in ('codigo_estacao', 'estacao', 'uf', 'latitude', 'longitude',
                            'VL_LATITUDE', 'VL_LONGITUDE') if c in colunas]
        diario = pd.read_parquet(clima_diario, columns=usar)
    else:
        diario = clima_diario
    mapa = (construir_mapa_estacao_microrregiao(diario)
            .rename(columns={'code_micro': 'CD_MICRO', 'name_micro': 'NM_MICRO'})
            [['codigo_estacao', 'CD_MICRO', 'NM_MICRO', 'origem']])
    if chave is not None:
        _CACHE_MAPA[chave] = mapa
    return mapa.copy()

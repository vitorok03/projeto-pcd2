import pandas as pd
import numpy as np
import geobr
import geopandas as gpd
import os

def ler_e_limpar_sidra(caminho_arquivo: str) -> pd.DataFrame:
    """(Mantido igual para leitura de CSV, caso queira usar no futuro)"""
    with open(caminho_arquivo, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()

    linha_variavel = lines[1].strip()
    if "Variável - " in linha_variavel:
        nome_variavel = linha_variavel.split("Variável - ")[1]
    else:
        nome_variavel = linha_variavel
    
    nome_variavel = nome_variavel.lower().replace(' ', '_').replace('(', '').replace(')', '').replace('ã', 'a').replace('ç', 'c').replace('é', 'e').replace('ó', 'o')

    linha_anos = lines[3].strip()
    colunas = [c.strip('"') for c in linha_anos.split(';')]
    anos = colunas[3:]

    dados = []
    for line in lines[5:]:
        line = line.strip()
        if not line or line.startswith('Fonte:'):
            break
        partes = line.split(';')
        if len(partes) < 4:
            continue
        partes = [p.strip('"') for p in partes]
        codigo = partes[1]
        municipio = partes[2]
        valores = partes[3:]
        
        for i, val in enumerate(valores):
            if i >= len(anos):
                break
            ano = anos[i]
            dados.append([codigo, municipio, ano, val])

    df = pd.DataFrame(dados, columns=['codigo_muni', 'municipio', 'ano', 'valor'])
    df['variavel'] = nome_variavel

    df['valor'] = df['valor'].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False).replace(['-', '...', 'X', 'nan'], np.nan)
    df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
    
    df = df.dropna(subset=['codigo_muni', 'ano', 'valor'])
    df['ano'] = pd.to_numeric(df['ano'], errors='coerce').dropna().astype(int)
    df['codigo_muni'] = pd.to_numeric(df['codigo_muni'], errors='coerce').dropna().astype(int).astype(str)

    return df

def agregar_para_microrregiao(df_long: pd.DataFrame) -> pd.DataFrame:
    """Agrega municípios em microrregiões e calcula o rendimento."""
    # 1. Carrega mapas do geobr
    gdf_muni = geobr.read_municipality(year=2020)
    gdf_micro = geobr.read_micro_region(year=2020)
    
    gdf_muni = gdf_muni.to_crs(epsg=4326)
    gdf_micro = gdf_micro.to_crs(epsg=4326)
    
    # 2. Join espacial usando centróides
    gdf_muni_metric = gdf_muni.to_crs(epsg=3857)
    gdf_muni_metric['geometry'] = gdf_muni_metric.geometry.centroid
    gdf_muni_cent = gdf_muni_metric.to_crs(epsg=4326)
    
    mapping = gpd.sjoin(
        gdf_muni_cent[['code_muni', 'geometry']], 
        gdf_micro[['code_micro', 'name_micro', 'geometry']], 
        how='inner', predicate='within'
    )
    
    de_para = pd.DataFrame(mapping[['code_muni', 'code_micro', 'name_micro']])
    de_para['code_muni'] = de_para['code_muni'].astype(int).astype(str)
    de_para['code_micro'] = de_para['code_micro'].astype(int).astype(str) # Força int para o CD_MICRO sair sem ".0"
    
    df_long['codigo_muni'] = df_long['codigo_muni'].astype(str).str.strip()
    
    # 3. Merge com o SIDRA
    df_merged = df_long.merge(de_para, left_on='codigo_muni', right_on='code_muni', how='inner')
    
    # 4. Pivotar
    df_pivot = df_merged.pivot_table(
        index=['code_micro', 'name_micro', 'ano'],
        columns='variavel',
        values='valor',
        aggfunc='first'
    ).reset_index()
    
    df_pivot.columns.name = None
    
    # 5. Agregação por Microrregião e Ano
    # Remover colunas de percentual (não fazem sentido após somar)
    colunas_pct = [c for c in df_pivot.columns if 'percentual' in c]
    df_pivot = df_pivot.drop(columns=colunas_pct, errors='ignore')
    
    # Identifica colunas para somar (excluindo as chaves e o rendimento_medio que vamos recalcular)
    chaves = ['code_micro', 'name_micro', 'ano']
    colunas_soma = [
        c for c in df_pivot.columns 
        if c not in chaves and 'rendimento_medio' not in c
    ]
    
    df_micro = df_pivot.groupby(chaves)[colunas_soma].sum(min_count=1).reset_index()
    
    # 6. Cálculo do Rendimento (em kg/ha)
    # Encontra as colunas com tolerância a acentos
    def achar_coluna(termos):
        for c in df_micro.columns:
            for t in termos:
                if t in c.lower():
                    return c
        return None
    
    col_area = achar_coluna(['colhida'])
    col_prod = achar_coluna(['quantidade', 'produzida'])
    
    if col_area and col_prod:
        # Produção (toneladas) / Área (hectares) * 1000 = kg/ha
        df_micro['rendimento_recalculado'] = np.where(
            df_micro[col_area] > 0,
            (df_micro[col_prod] * 1000) / df_micro[col_area],
            np.nan
        )
    else:
        print(f"\n⚠️ Não foi possível achar colunas de área/produção. Colunas: {df_micro.columns.tolist()}")
        df_micro['rendimento_recalculado'] = np.nan

    df_micro = df_micro.rename(columns={'code_micro': 'CD_MICRO', 'name_micro': 'NM_MICRO'})
    return df_micro

def processar_dados_sidra(caminho_arquivo: str) -> pd.DataFrame:
    """Pipeline completo de processamento da Soja via CSV."""
    df_long = ler_e_limpar_sidra(caminho_arquivo)
    df_micro = agregar_para_microrregiao(df_long)
    return df_micro
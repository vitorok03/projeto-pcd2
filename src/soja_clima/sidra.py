"""Leitura e preparação da produção de soja do SIDRA (Tabela 1612)."""
from io import StringIO

import numpy as np
import pandas as pd


def ler_sidra_soja(path):
    """Lê um arquivo do SIDRA (tabela 1612, PAM MUNICÍPIO) e retorna uma
    tabela limpa em nível de município, com UF extraída do nome."""
    with open(path, encoding='utf-8-sig') as f:
        linhas = f.readlines()

    idx_fonte = next(i for i, l in enumerate(linhas) if l.startswith('"Fonte:'))

    # Corte manual em vez de skipfooter: o rodapé de notas do SIDRA tem
    # campos com quebra de linha dentro de aspas, o que faz o skipfooter
    # (baseado em contagem de linhas físicas) remover linhas de dado a mais.
    bloco = ''.join(linhas[2:idx_fonte])
    df = pd.read_csv(StringIO(bloco), sep=';', quotechar='"')

    extraido = df['Município'].str.extract(r'^(.*) \(([A-Z]{2})\)$')
    df['municipio'] = extraido[0]
    df['uf'] = extraido[1]

    df = df.rename(columns={
        'Ano': 'ano',
        'Área plantada (Hectares)': 'area_plantada_ha',
        'Área colhida (Hectares)': 'area_colhida_ha',
        'Quantidade produzida (Toneladas)': 'producao_ton',
        'Rendimento médio da produção (Quilogramas por Hectare)': 'rendimento_kg_ha',
    })

    colunas_numericas = ['area_plantada_ha', 'area_colhida_ha', 'producao_ton', 'rendimento_kg_ha']
    for col in colunas_numericas:
        if not pd.api.types.is_numeric_dtype(df[col]):
            df[col] = (df[col].astype(str).str.strip()
                       .replace({'-': np.nan, '..': np.nan, '...': np.nan, 'X': np.nan})
                       .str.replace('.', '', regex=False)
                       .str.replace(',', '.', regex=False)
                       .astype(float))

    return df[['municipio', 'uf', 'ano', 'area_plantada_ha', 'area_colhida_ha',
                'producao_ton', 'rendimento_kg_ha']]


def agregar_soja_para_microrregiao(producao_soja_com_micro):
    """Usar quando a soja vem por MUNICÍPIO (não já por microrregião) --
    soma é necessária aqui porque vários municípios se combinam numa
    microrregião. Rendimento NÃO é média dos rendimentos municipais --
    é recalculado a partir das somas (senão municípios pequenos pesariam
    igual a grandes)."""
    agg = producao_soja_com_micro.groupby(['code_micro', 'ano']).agg(
        area_plantada_ha=('area_plantada_ha', 'sum'),
        area_colhida_ha=('area_colhida_ha', 'sum'),
        producao_ton=('producao_ton', 'sum'),
        n_municipios=('municipio', 'nunique'),
    ).reset_index()

    agg['rendimento_kg_ha'] = np.where(
        agg['area_colhida_ha'] > 0,
        (agg['producao_ton'] * 1000) / agg['area_colhida_ha'],
        np.nan,
    )
    return agg


def preparar_soja_microrregiao(df):
    """Usar quando o SIDRA já foi exportado agregado por microrregião
    (ex: após join com geobr por 'Microrregião Geográfica'). NÃO soma
    nada -- cada linha já deveria ser (microrregião, ano). Em vez de
    assumir isso, verifica: (1) se não há duplicidade escondida na
    exportação, e (2) se o rendimento informado bate com produção/área,
    como checagem cruzada de que o parsing dos números está correto."""
    df = df.rename(columns={
        'Ano': 'ano',
        'Área plantada (Hectares)': 'area_plantada_ha',
        'Área colhida (Hectares)': 'area_colhida_ha',
        'Quantidade produzida (Toneladas)': 'producao_ton',
        'Rendimento médio da produção (Quilogramas por Hectare)': 'rendimento_kg_ha_sidra',
    })

    colunas_numericas = ['area_plantada_ha', 'area_colhida_ha', 'producao_ton', 'rendimento_kg_ha_sidra']
    for col in colunas_numericas:
        # is_numeric_dtype em vez de checar "== object": em algumas
        # versões do pandas, colunas de texto são reportadas como dtype
        # "str" em vez do "object" clássico.
        if not pd.api.types.is_numeric_dtype(df[col]):
            df[col] = (df[col].astype(str).str.strip()
                       .replace({'-': np.nan, '..': np.nan, '...': np.nan, 'X': np.nan})
                       .str.replace('.', '', regex=False)
                       .str.replace(',', '.', regex=False)
                       .astype(float))

    df['ano'] = pd.to_numeric(df['ano'], errors='coerce').astype('Int64')

    contagem = df.groupby(['code_micro', 'ano']).size()
    duplicados = contagem[contagem > 1]
    if len(duplicados) > 0:
        print(f"ATENÇÃO: {len(duplicados)} combinação(ões) code_micro-ano duplicada(s) "
              "-- a soma NÃO é dispensável neste arquivo.")
    else:
        print("OK: cada (code_micro, ano) aparece exatamente uma vez.")

    df['rendimento_kg_ha_calc'] = np.where(
        df['area_colhida_ha'] > 0,
        (df['producao_ton'] * 1000) / df['area_colhida_ha'],
        np.nan,
    )
    diff = (df['rendimento_kg_ha_calc'] - df['rendimento_kg_ha_sidra']).abs()
    divergentes = df[diff > 1]
    if len(divergentes) > 0:
        print(f"ATENÇÃO: {len(divergentes)} linha(s) onde o rendimento recalculado "
              "diverge do informado pelo SIDRA (checar parsing).")
    else:
        print("OK: rendimento recalculado bate com o do SIDRA em todas as linhas.")

    colunas_finais = ['code_micro', 'name_micro', 'abbrev_state', 'ano',
                       'area_plantada_ha', 'area_colhida_ha', 'producao_ton', 'rendimento_kg_ha_sidra']
    return df[colunas_finais].rename(columns={'rendimento_kg_ha_sidra': 'rendimento_kg_ha'})

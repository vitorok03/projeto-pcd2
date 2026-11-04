"""Leitura, limpeza e agregação horária->diária dos arquivos do INMET.

Só definições reutilizáveis aqui -- nenhum caminho de arquivo real,
nenhuma execução. Quem chama essas funções com os arquivos de verdade
é o notebook de orquestração (ex: notebooks/01_uniao_climatica.ipynb).
"""
import numpy as np
import pandas as pd
import os
import shutil
import time

# Nomes de coluna em maiúsculo -> nome canônico. A comparação é sempre
# feita em maiúsculo, o que já resolve variações como
# 'RADIACAO GLOBAL (KJ/m²)' (2015/2019) vs 'RADIACAO GLOBAL (Kj/m²)' (2020+).
COLUNAS_CONHECIDAS = {
    'PRECIPITAÇÃO TOTAL, HORÁRIO (MM)': 'precipitacao',
    'TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)'.upper(): 'temperatura',
    'TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)'.upper(): 'temp_max_hora',
    'TEMPERATURA MÍNIMA NA HORA ANT. (AUT) (°C)'.upper(): 'temp_min_hora',
    'UMIDADE RELATIVA DO AR, HORARIA (%)': 'umidade',
    'RADIACAO GLOBAL (KJ/M²)': 'radiacao',
    'VENTO, VELOCIDADE HORARIA (M/S)': 'vento',
}

COLUNAS_ESSENCIAIS = {'data', 'hora', 'precipitacao', 'temperatura', 'temp_max_hora',
                       'temp_min_hora', 'umidade', 'radiacao', 'vento'}


def copiar_um_arquivo(origem, destino, tentativas=3):
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    for _ in range(tentativas):
        try:
            shutil.copy2(origem, destino)
            return True
        except Exception:
            time.sleep(2)
    return False


def normalizar_chave_meta(chave):
    """A partir de 2019 o INMET passou a exportar alguns cabeçalhos com
    caracteres corrompidos (ex: 'ESTAC?O' em vez de 'ESTAÇÃO'). Normaliza
    as variantes conhecidas para uma chave única."""
    chave = chave.strip().upper()
    correcoes = {
        'REGI?O': 'REGIAO', 'REGIÃO': 'REGIAO',
        'ESTAC?O': 'ESTACAO', 'ESTAÇÃO': 'ESTACAO',
        'DATA DE FUNDAC?O': 'DATA DE FUNDACAO', 'DATA DE FUNDAÇÃO': 'DATA DE FUNDACAO',
    }
    return correcoes.get(chave, chave)


def ler_arquivo_inmet(path):
    """Lê um único CSV do INMET (formato padrão de estação automática)
    e retorna um dataframe horário limpo, com metadados da estação.
    Compatível com o formato antigo (até ~2018) e os formatos 2019+, que
    mudaram nomes de coluna (inclusive maiúscula/minúscula) e corromperam
    alguns cabeçalhos de metadados. Levanta erro claro se alguma coluna
    essencial não for encontrada."""
    meta = {}
    with open(path, encoding='latin1') as f:
        for _ in range(8):
            linha = f.readline().strip()
            chave, valor = linha.split(':;')
            meta[normalizar_chave_meta(chave)] = valor.strip()

    df = pd.read_csv(path, sep=';', encoding='latin1', skiprows=8, decimal=',')
    df = df.loc[:, ~df.columns.str.startswith('Unnamed')]

    mapa_renomeacao = {}
    for col in df.columns:
        col_upper = col.strip().upper()
        if col_upper.startswith('DATA'):
            mapa_renomeacao[col] = 'data'
        elif col_upper.startswith('HORA'):
            mapa_renomeacao[col] = 'hora'
        elif col_upper in COLUNAS_CONHECIDAS:
            mapa_renomeacao[col] = COLUNAS_CONHECIDAS[col_upper]

    df = df.rename(columns=mapa_renomeacao)

    faltando = COLUNAS_ESSENCIAIS - set(df.columns)
    if faltando:
        raise ValueError(f"Colunas essenciais não encontradas em {path}: {faltando}")

    df['data'] = pd.to_datetime(df['data'])

    colunas_numericas = df.select_dtypes(include=[np.number]).columns
    df[colunas_numericas] = df[colunas_numericas].replace(-9999, np.nan)

    # Radiação: -9999 à noite geralmente significa 0, não ausência real
    hora_num = df['hora'].astype(str).str.strip().str.slice(0, 2).astype(int)
    noite = (hora_num < 9) | (hora_num > 19)
    df.loc[df['radiacao'].isna() & noite, 'radiacao'] = 0
    df['radiacao'] = df['radiacao'].clip(lower=0)

    df['codigo_estacao'] = meta['CODIGO (WMO)']
    df['uf'] = meta['UF']
    df['estacao'] = meta['ESTACAO']
    df['latitude'] = float(meta['LATITUDE'].replace(',', '.'))
    df['longitude'] = float(meta['LONGITUDE'].replace(',', '.'))

    return df


def agregar_diario(df_horario):
    """Agrega um dataframe HORÁRIO (já lido por ler_arquivo_inmet) para
    1 linha por dia, para a mesma estação."""
    diario = df_horario.groupby(
        ['codigo_estacao', 'uf', 'estacao', 'latitude', 'longitude', 'data']
    ).agg(
        prec_total=('precipitacao', 'sum'),
        temp_media=('temperatura', 'mean'),
        temp_max=('temp_max_hora', 'max'),
        temp_min=('temp_min_hora', 'min'),
        umid_media=('umidade', 'mean'),
        radiacao_total=('radiacao', 'sum'),
        vento_medio=('vento', 'mean'),
        n_horas_validas=('temperatura', 'count'),
    ).reset_index()

    diario['amplitude_termica'] = diario['temp_max'] - diario['temp_min']
    diario['dia_seco'] = diario['prec_total'] < 1
    diario['gdd'] = ((diario['temp_max'] + diario['temp_min']) / 2 - 10).clip(lower=0)

    return diario


def ler_e_agregar_diario(path, horas_minimas_validas=18):
    """Atalho: lê um arquivo e já entrega o diário, descartando dias com
    poucas horas válidas (controle de qualidade básico)."""
    df_horario = ler_arquivo_inmet(path)
    diario = agregar_diario(df_horario)
    return diario[diario['n_horas_validas'] >= horas_minimas_validas].copy()

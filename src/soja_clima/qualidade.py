"""Diagnósticos de qualidade dos dados climáticos: faixas plausíveis,
gaps, valores repetidos suspeitos e estações fora do território
brasileiro (ex: a estação antártica do INMET, com metadado de UF
incorreto no cabeçalho)."""
import numpy as np
import pandas as pd

from .inmet import ler_arquivo_inmet

# Faixas fisicamente plausíveis para o Brasil -- ajuste se tiver estações
# em regiões com extremos conhecidos (ex: Sul tem mínimas mais baixas).
FAIXAS_PLAUSIVEIS = {
    'temperatura': (-10, 45),
    'precipitacao': (0, 150),   # mm em 1 hora
    'umidade': (0, 100),
    'vento': (0, 40),           # m/s
}

# Caixa geográfica aproximada do Brasil continental. Usada para excluir
# estações com coordenada fora do país (ex: a estação antártica do
# INMET, cujo cabeçalho traz "UF: SP" por erro de metadado, mas cujas
# coordenadas reais são -84/-79 -- muito ao sul de qualquer ponto do
# Brasil).
BRASIL_LAT = (-34, 6)
BRASIL_LON = (-74, -32)


def filtrar_estacoes_fora_do_brasil(df, coluna_lat='latitude', coluna_lon='longitude'):
    """Remove linhas cuja coordenada cai fora da caixa geográfica do
    Brasil. Retorna (df_filtrado, df_removido) -- inspecione o segundo
    antes de descartar, para confirmar que são mesmo os casos esperados."""
    dentro = (df[coluna_lat].between(*BRASIL_LAT) & df[coluna_lon].between(*BRASIL_LON))
    return df[dentro].copy(), df[~dentro].copy()


def detectar_sequencias_repetidas(df, coluna, min_repeticoes=3):
    """Sinaliza sequências de valor IDÊNTICO se repetindo por várias
    linhas seguidas na mesma coluna -- assinatura comum de sensor
    travado/saturado, não fenômeno real (ex: temp_max = 45.0°C em 3 dias
    seguidos no inverno). Espera-se que `df` já esteja ordenado por data
    e filtrado para uma única estação antes de chamar esta função."""
    valores = df[coluna]
    grupo_mudou = (valores != valores.shift()).cumsum()
    tamanhos = valores.groupby(grupo_mudou).transform('size')
    suspeitos = df[(tamanhos >= min_repeticoes) & valores.notna()].copy()
    suspeitos['tamanho_sequencia'] = tamanhos[(tamanhos >= min_repeticoes) & valores.notna()]
    return suspeitos


def diagnosticar_arquivo(path):
    """Diagnóstico leve de UM arquivo: completude, valores fora de faixa
    física, maior gap contínuo. Pensado para rodar em milhares de
    arquivos sem guardar os dados horários brutos em memória -- só o
    resumo (1 linha) é retornado."""
    df = ler_arquivo_inmet(path)

    diag = {
        'arquivo': path.split('/')[-1],
        'codigo_estacao': df['codigo_estacao'].iloc[0],
        'estacao': df['estacao'].iloc[0],
        'uf': df['uf'].iloc[0],
        'latitude': df['latitude'].iloc[0],
        'longitude': df['longitude'].iloc[0],
        'ano': df['data'].dt.year.mode()[0],
        'n_horas': len(df),
        'periodo_min': df['data'].min(),
        'periodo_max': df['data'].max(),
    }

    for var in ['temperatura', 'precipitacao', 'umidade', 'vento', 'radiacao']:
        diag[f'{var}_pct_faltante'] = round(df[var].isna().mean() * 100, 1)

    for var, (lo, hi) in FAIXAS_PLAUSIVEIS.items():
        fora = ((df[var] < lo) | (df[var] > hi)).sum()
        diag[f'{var}_fora_faixa'] = int(fora)

    faltando = df['temperatura'].isna()
    grupos = (~faltando).cumsum()
    maior_gap = faltando.groupby(grupos).sum().max() if faltando.any() else 0
    diag['maior_gap_horas_temp'] = int(maior_gap)

    return diag

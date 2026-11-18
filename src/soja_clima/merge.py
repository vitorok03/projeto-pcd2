"""Merge final entre clima e produção e preparação da base de modelagem.

Orquestrado por `main.ipynb` (pipeline único):
- `montar_base_final` (contrato da main): clima e produção já agregados
  por microrregião-safra/ano, chave `code_micro` (inner join).
- `agregar_clima_micro_safra` / `agregar_pacifico_safra`: totais da safra
  inteira e índices do Pacífico, complementares às fases fenológicas.
- `adicionar_solo`, `filtrar_base_modelagem`, `selecionar_colunas_solo`,
  `calcular_desvio_clima`: etapas finais vindas da refatoração.

A agregação climática é SEMPRE a da main (`agregacao.py`):
1. temporal, dentro de cada estação, na janela da safra
   (1/set do ano anterior + 240 dias, rotulada pelo ano da colheita --
   o mesmo `ano` do PAM/SIDRA), com limiar de completude;
2. espacial, entre as estações da microrregião, por MÉDIA ponderada pela
   completude (extremos = max/min entre estações).

Antes, a refatoração somava todos os dias de todas as estações da
microrregião, o que multiplicava precipitação, GDD e dias secos pelo
número de estações (ex.: 13.764 mm/ano, 2.985 dias secos num ano).
"""
from __future__ import annotations

from os import PathLike
from typing import Iterable

import numpy as np
import pandas as pd

from .agregacao import (
    agregar_diario_para_estacao_safra,
    agregar_espacial_para_microrregiao,
)
from .qualidade import filtrar_estacoes_fora_do_brasil

DIAS_JANELA_SAFRA = 241  # 1/set + 240 dias (mesma janela de agregacao.py)
MESES_SAFRA = [9, 10, 11, 12, 1, 2, 3, 4]  # mesma janela, em meses (Pacífico)

# Limpeza física dos sensores (Alerta 6 da EDA, vinda de correcoes_filtros)
LIMITES_FISICOS = {'temp_min_min': -10, 'prec_total_max': 300, 'gdd_max': 35}

# nome na agregação da main -> nome usado na base da refatoração
_RENOMEAR_CLIMA = {
    'prec_total_safra_completa': 'precipitacao_total',
    'dias_secos_safra_completa': 'dias_secos_total',
    'temp_media_safra_completa': 'temp_media_anual',
    'temp_max_abs_safra_completa': 'temp_max_anual',
    'temp_min_abs_safra_completa': 'temp_min_anual',
    'gdd_acumulado_safra_completa': 'gdd_total',
    'amplitude_media_safra_completa': 'amplitude_media',
    'radiacao_media_safra_completa': 'radiacao_media',
    'completude_safra_completa': 'completude',
}


def montar_base_final(clima_micro_safra: pd.DataFrame, producao_micro_ano: pd.DataFrame) -> pd.DataFrame:
    """Inner join: uma linha só é útil para o modelo se tiver os dois
    lados (clima e produção) para o mesmo (microrregião, ano)."""
    return producao_micro_ano.merge(
        clima_micro_safra,
        left_on=['code_micro', 'ano'],
        right_on=['code_micro', 'safra'],
        how='inner',
    )


def _padronizar_cd_micro(serie: pd.Series) -> pd.Series:
    """'5101.0' / 5101.0 / '5101' -> '5101' (string sem '.0')."""
    return serie.astype(str).str.replace(r'\.0$', '', regex=True).str.strip()


def agregar_clima_micro_safra(
    df_clima: pd.DataFrame,
    df_mapa: pd.DataFrame,
    aplicar_limites_fisicos: bool = True,
) -> pd.DataFrame:
    """Clima diário (formato da refatoração, colunas VL_LATITUDE/VL_LONGITUDE
    ou latitude/longitude) + mapa estação->microrregião (CD_MICRO ou
    code_micro) -> uma linha por (CD_MICRO, ano-safra).

    Colunas de saída (nomes mantidos da refatoração por compatibilidade,
    mas agora são da SAFRA, não do ano civil): precipitacao_total,
    dias_secos_total, temp_media_anual, temp_max_anual, temp_min_anual,
    gdd_total, amplitude_media, radiacao_media, completude, n_estacoes,
    n_dias_validos, taxa_chuva_diaria, fracao_dias_secos, gdd_medio_diario.
    """
    clima = df_clima.copy()
    mapa = df_mapa.copy()

    col_lat = 'VL_LATITUDE' if 'VL_LATITUDE' in clima.columns else 'latitude'
    col_lon = 'VL_LONGITUDE' if 'VL_LONGITUDE' in clima.columns else 'longitude'
    clima, removidas = filtrar_estacoes_fora_do_brasil(clima, coluna_lat=col_lat, coluna_lon=col_lon)
    if len(removidas):
        print(f"  - {len(removidas)} registros de estações fora do Brasil removidos")

    if aplicar_limites_fisicos:
        antes = len(clima)
        clima = clima[
            (clima['temp_min'] >= LIMITES_FISICOS['temp_min_min'])
            & (clima['prec_total'] <= LIMITES_FISICOS['prec_total_max'])
            & (clima['gdd'] <= LIMITES_FISICOS['gdd_max'])
        ].copy()
        print(f"  - {antes - len(clima)} dias removidos pelos limites físicos")

    col_micro = 'CD_MICRO' if 'CD_MICRO' in mapa.columns else 'code_micro'
    mapa = mapa.dropna(subset=[col_micro])
    mapa = pd.DataFrame({
        'codigo_estacao': mapa['codigo_estacao'].astype(str),
        'code_micro': _padronizar_cd_micro(mapa[col_micro]),
    }).drop_duplicates()

    clima['codigo_estacao'] = clima['codigo_estacao'].astype(str)
    clima['data'] = pd.to_datetime(clima['data'])
    clima_micro = clima.merge(mapa, on='codigo_estacao', how='inner')

    estacao_safra = agregar_diario_para_estacao_safra(clima_micro, usar_fases=False)
    micro_safra = agregar_espacial_para_microrregiao(estacao_safra, fases=['safra_completa'])

    micro_safra = micro_safra.rename(columns={**_RENOMEAR_CLIMA, 'code_micro': 'CD_MICRO', 'safra': 'ano'})
    micro_safra['ano'] = micro_safra['ano'].astype(int)

    # Taxas por dia observado (a completude média estima a fração de dias
    # com dado; as somas da main são sobre os dias observados).
    micro_safra['n_dias_validos'] = (micro_safra['completude'] * DIAS_JANELA_SAFRA).round()
    dias = micro_safra['n_dias_validos'].where(micro_safra['n_dias_validos'] > 0)
    micro_safra['taxa_chuva_diaria'] = micro_safra['precipitacao_total'] / dias
    micro_safra['fracao_dias_secos'] = micro_safra['dias_secos_total'] / dias
    micro_safra['gdd_medio_diario'] = micro_safra['gdd_total'] / dias
    return micro_safra


def agregar_pacifico_safra(df_pacifico: pd.DataFrame, meses: Iterable[int] = MESES_SAFRA) -> pd.DataFrame:
    """ONI/SOI mensal -> média na janela da safra, rotulada pelo ano da
    colheita (set-dez contam para o ano seguinte), como em agregacao.ano_safra."""
    p = df_pacifico.copy()
    p['ano'] = p['ano'].astype(int)
    p['mes'] = p['mes'].astype(int)
    p = p[p['mes'].isin(meses)].copy()
    p['ano_safra'] = np.where(p['mes'] >= 9, p['ano'] + 1, p['ano'])
    return (p.groupby('ano_safra')
             .agg(oni_medio=('oni', 'mean'), soi_medio=('soi', 'mean'))
             .reset_index()
             .rename(columns={'ano_safra': 'ano'}))


SOLO_COLUNAS_MANTER = [
    'phh2o_0-5cm_mean',   # pH (x10)
    'clay_0-5cm_mean',    # argila (g/kg)
    'sand_0-5cm_mean',    # areia (g/kg)
    'soc_0-5cm_mean',     # carbono orgânico (dg/kg)
    'cec_0-5cm_mean',     # capacidade de troca catiônica
    'bdod_0-5cm_mean',    # densidade do solo
    'wv0033_0-5cm_mean',  # água disponível
]
_PREFIXOS_SOLO = ('clay', 'sand', 'silt', 'bdod', 'soc', 'cec', 'phh2o', 'wv0033')


def adicionar_solo(base: pd.DataFrame, df_solo: pd.DataFrame) -> pd.DataFrame:
    """Left join do solo estático (SoilGrids, uma linha por microrregião).
    Cria `CD_MICRO` (string) a partir de `code_micro` se ainda não existir."""
    base = base.copy()
    if 'CD_MICRO' not in base.columns:
        base['CD_MICRO'] = _padronizar_cd_micro(base['code_micro'])
    solo = df_solo.dropna(subset=['CD_MICRO']).copy()
    solo['CD_MICRO'] = _padronizar_cd_micro(solo['CD_MICRO'])
    return base.merge(solo, on='CD_MICRO', how='left')


def selecionar_colunas_solo(base: pd.DataFrame, manter: Iterable[str] = SOLO_COLUNAS_MANTER) -> pd.DataFrame:
    """Remove variáveis de solo redundantes (multicolinearidade entre
    camadas de profundidade), mantendo só as da camada 0-5cm em `manter`."""
    solo = [c for c in base.columns if c.startswith(_PREFIXOS_SOLO)]
    return base.drop(columns=[c for c in solo if c not in manter])


def filtrar_base_modelagem(
    base: pd.DataFrame,
    area_min_ha: float = 100,
    rendimento_max_kg_ha: float = 6000,
    ano_min: int = 2009,
) -> pd.DataFrame:
    """Filtros da EDA: área colhida mínima (ruído de áreas pequenas),
    rendimento fisicamente plausível para soja comercial e corte temporal
    (antes de 2009, > 25% do clima ausente). Imprime quantas linhas cada
    filtro removeu."""
    etapas = [
        (f'área colhida < {area_min_ha} ha (ou sem soja)', base['area_colhida_ha'] >= area_min_ha),
        (f'rendimento > {rendimento_max_kg_ha} kg/ha', base['rendimento_kg_ha'] <= rendimento_max_kg_ha),
        (f'ano < {ano_min}', base['ano'] >= ano_min),
    ]
    mascara = pd.Series(True, index=base.index)
    for nome, cond in etapas:
        removidas = (mascara & ~cond).sum()
        mascara &= cond
        print(f"  - removidas {removidas} linhas: {nome}")
    return base[mascara].copy()


def calcular_desvio_clima(base: pd.DataFrame, grau: int = 2) -> pd.DataFrame:
    """Detrending da tendência tecnológica: ajusta um polinômio (grau 2) ao
    rendimento NACIONAL ponderado pela área de cada ano e devolve a base
    com `rendimento_tendencia` e `desvio_clima` (= rendimento nacional do
    ano - tendência), como no antigo `correcoes_filtros`.

    ATENÇÃO: o desvio é o mesmo para todas as microrregiões do ano (um
    valor por ano)."""
    nacional = (base.groupby('ano')
                    .apply(lambda x: x['producao_ton'].sum() * 1000 / x['area_colhida_ha'].sum(),
                           include_groups=False)
                    .rename('rendimento_nacional').reset_index())
    anos = nacional['ano'].to_numpy(dtype=float)
    centro = anos.mean()  # centraliza para estabilidade numérica (mesmo ajuste)
    coef = np.polyfit(anos - centro, nacional['rendimento_nacional'], grau)
    nacional['rendimento_tendencia'] = np.polyval(coef, anos - centro)
    nacional['desvio_clima'] = nacional['rendimento_nacional'] - nacional['rendimento_tendencia']
    base = base.drop(columns=['rendimento_tendencia', 'desvio_clima'], errors='ignore')
    return base.merge(nacional[['ano', 'rendimento_tendencia', 'desvio_clima']], on='ano', how='left')


# Nomes da base final (contrato da main) -> nomes usados nos notebooks de EDA
NOMES_EDA = {
    'producao_ton': 'quantidade_produzida',
    'area_colhida_ha': 'área_colhida',
    'area_plantada_ha': 'área_plantada',
    'rendimento_kg_ha': 'rendimento_recalculado',
}


# Colunas derivadas que algumas análises recalculam por conta própria
COLUNAS_DESVIO = ('desvio_clima', 'rendimento_tendencia')
COLUNAS_TAXAS_DIARIAS = ('n_dias_validos', 'taxa_chuva_diaria', 'fracao_dias_secos', 'gdd_medio_diario')
# Colunas novas da base única que os notebooks de EDA calculam com o mesmo nome
COLUNAS_RECALCULADAS_EDA = ('amplitude_media', 'radiacao_media')


def carregar_base_final(
    caminho: str | PathLike,
    nomes_eda: bool = True,
    descartar: Iterable[str] = (),
) -> pd.DataFrame:
    """Lê a base única do projeto (`data/processed/base_final_modelagem.csv`,
    gerada pelo main.ipynb) com `CD_MICRO` como string. Com `nomes_eda=True`
    devolve as colunas de soja com os nomes usados nos notebooks de EDA
    (e omite `COLUNAS_RECALCULADAS_EDA`, que a EDA recalcula).
    `descartar` remove colunas derivadas que a análise vai recalcular (ex.:
    `COLUNAS_DESVIO`), para o merge dela não gerar sufixos _x/_y."""
    base = pd.read_csv(caminho, dtype={'CD_MICRO': str})
    if nomes_eda:
        descartar = (*descartar, *COLUNAS_RECALCULADAS_EDA)
    base = base.drop(columns=list(descartar), errors='ignore')
    return base.rename(columns=NOMES_EDA) if nomes_eda else base

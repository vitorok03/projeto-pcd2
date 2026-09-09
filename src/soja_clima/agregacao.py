"""Agregação temporal (diário -> estação-safra) e espacial (estação ->
microrregião). Ver o notebook de agregação para a explicação de por que
soma/média se comportam diferente nas duas direções."""
import numpy as np
import pandas as pd

# Dias esperados em cada fase (derivado dos limiares usados em
# fase_fenologica: plantio 0-39, vegetativo 40-89,
# floracao_enchimento 90-129, maturacao 130-240).
DIAS_ESPERADOS_FASE = {
    'plantio': 40,
    'vegetativo': 50,
    'floracao_enchimento': 40,
    'maturacao': 111,
}

LIMIAR_COMPLETUDE = 0.80  # abaixo disso, o valor agregado vira NaN


def ano_safra(data):
    return data.year if data.month < 9 else data.year + 1


def fase_fenologica(data, safra):
    inicio = pd.Timestamp(safra - 1, 9, 1)
    dias = (data - inicio).days
    if dias < 0 or dias > 240:
        return None
    if dias < 40:
        return 'plantio'
    elif dias < 90:
        return 'vegetativo'
    elif dias < 130:
        return 'floracao_enchimento'
    else:
        return 'maturacao'


def agregar_diario_para_estacao_safra(diario_com_micro, usar_fases=True):
    """Agregação TEMPORAL (dentro da mesma estação): soma continua soma,
    média continua média, extremo continua extremo. A completude decide
    se o resultado é confiável (vira NaN abaixo do limiar).

    usar_fases=False agrega a safra inteira como um único período (bom
    para um baseline inicial); usar_fases=True quebra em
    plantio/vegetativo/floração-enchimento/maturação."""
    df = diario_com_micro.copy()
    df['safra'] = df['data'].apply(ano_safra)

    if usar_fases:
        df['fase'] = df.apply(lambda r: fase_fenologica(r['data'], r['safra']), axis=1)
        df = df.dropna(subset=['fase']).copy()
    else:
        inicio_janela = df['data'].apply(lambda d: pd.Timestamp(ano_safra(d) - 1, 9, 1))
        dentro_da_janela = (df['data'] - inicio_janela).dt.days.between(0, 240)
        df = df[dentro_da_janela].copy()
        df['fase'] = 'safra_completa'

    agg = df.groupby(['codigo_estacao', 'code_micro', 'safra', 'fase']).agg(
        prec_total=('prec_total', 'sum'),
        dias_secos=('dia_seco', 'sum'),
        temp_media=('temp_media', 'mean'),
        temp_max_abs=('temp_max', 'max'),
        temp_min_abs=('temp_min', 'min'),
        gdd_acumulado=('gdd', 'sum'),
        amplitude_media=('amplitude_termica', 'mean'),
        radiacao_media=('radiacao_total', 'mean'),
        dias_observados=('data', 'count'),
    ).reset_index()

    dias_esperados_map = DIAS_ESPERADOS_FASE if usar_fases else {'safra_completa': 241}
    agg['dias_esperados'] = agg['fase'].map(dias_esperados_map)
    agg['completude'] = (agg['dias_observados'] / agg['dias_esperados']).clip(upper=1.0)

    colunas_estatisticas = ['prec_total', 'dias_secos', 'temp_media', 'temp_max_abs',
                             'temp_min_abs', 'gdd_acumulado', 'amplitude_media', 'radiacao_media']
    abaixo_limiar = agg['completude'] < LIMIAR_COMPLETUDE
    agg.loc[abaixo_limiar, colunas_estatisticas] = np.nan

    pivot = agg.pivot_table(
        index=['codigo_estacao', 'code_micro', 'safra'],
        columns='fase',
        values=colunas_estatisticas + ['completude'],
    )
    pivot.columns = [f"{a}_{b}" for a, b in pivot.columns]
    return pivot.reset_index()


def agregar_espacial_para_microrregiao(base_estacao_safra, fases=None):
    """Agregação ESPACIAL (entre estações da mesma microrregião): soma e
    média viram média PONDERADA pela completude; extremo continua sendo
    max/min entre as estações (nunca uma média de extremos).

    `fases` deve bater com o que foi usado em
    agregar_diario_para_estacao_safra: None (padrão) = as 4 fases
    fenológicas; passe ['safra_completa'] se usar_fases=False lá."""
    fases = fases if fases is not None else list(DIAS_ESPERADOS_FASE.keys())
    colunas_media_ponderada = ['prec_total', 'dias_secos', 'temp_media',
                                'gdd_acumulado', 'amplitude_media', 'radiacao_media']
    colunas_extremo_max = ['temp_max_abs']
    colunas_extremo_min = ['temp_min_abs']

    def agregar_grupo(grupo):
        resultado = {}
        for fase in fases:
            col_completude = f'completude_{fase}'
            peso_base = grupo[col_completude] if col_completude in grupo else None

            for col in colunas_media_ponderada:
                nome_col = f'{col}_{fase}'
                if nome_col not in grupo:
                    continue
                valores = grupo[nome_col]
                validos = valores.notna()
                pesos = peso_base[validos] if peso_base is not None else pd.Series(1, index=valores[validos].index)
                resultado[nome_col] = ((valores[validos] * pesos).sum() / pesos.sum()) if pesos.sum() > 0 else np.nan

            for col in colunas_extremo_max:
                nome_col = f'{col}_{fase}'
                if nome_col in grupo:
                    resultado[nome_col] = grupo[nome_col].max()

            for col in colunas_extremo_min:
                nome_col = f'{col}_{fase}'
                if nome_col in grupo:
                    resultado[nome_col] = grupo[nome_col].min()

            if col_completude in grupo:
                resultado[col_completude] = grupo[col_completude].mean()

        resultado['n_estacoes'] = grupo['codigo_estacao'].nunique()
        return pd.Series(resultado)

    return (
        base_estacao_safra.groupby(['code_micro', 'safra'])
        .apply(agregar_grupo, include_groups=False)
        .reset_index()
    )

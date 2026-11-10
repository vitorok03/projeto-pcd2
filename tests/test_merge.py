import numpy as np
import pandas as pd

from soja_clima.merge import agregar_clima_micro_safra, agregar_pacifico_safra


def _diario_estacao(codigo, chuva_diaria, inicio='2019-09-01', dias=241):
    datas = pd.date_range(inicio, periods=dias, freq='D')
    return pd.DataFrame({
        'codigo_estacao': codigo,
        'data': datas,
        'VL_LATITUDE': -15.0,
        'VL_LONGITUDE': -50.0,
        'prec_total': chuva_diaria,
        'temp_media': 25.0,
        'temp_max': 30.0,
        'temp_min': 20.0,
        'gdd': 15.0,
        'dia_seco': int(chuva_diaria < 2),
        'amplitude_termica': 10.0,
        'radiacao_total': 20000.0,
    })


def test_clima_e_media_entre_estacoes_nao_soma():
    """Regressão do bug de inflação: duas estações na mesma microrregião
    devem dar a MÉDIA dos totais da safra, não a soma."""
    diario = pd.concat([_diario_estacao('A001', 4.0), _diario_estacao('A002', 6.0)])
    mapa = pd.DataFrame({'codigo_estacao': ['A001', 'A002'], 'CD_MICRO': [5101.0, 5101.0]})

    res = agregar_clima_micro_safra(diario, mapa)

    assert len(res) == 1
    linha = res.iloc[0]
    assert linha['CD_MICRO'] == '5101'
    assert linha['ano'] == 2020  # set/2019-abr/2020 -> safra (ano do SIDRA) 2020
    assert linha['n_estacoes'] == 2
    assert np.isclose(linha['precipitacao_total'], 241 * 5.0)  # média de 4 e 6 mm/dia
    assert np.isclose(linha['gdd_total'], 241 * 15.0)
    assert linha['n_dias_validos'] <= 241
    assert np.isclose(linha['taxa_chuva_diaria'], 5.0)


def test_pacifico_usa_janela_da_safra():
    meses = pd.DataFrame({'ano': [2019] * 12 + [2020] * 12,
                          'mes': list(range(1, 13)) * 2})
    meses['oni'] = np.where(meses['mes'].isin([9, 10, 11, 12, 1, 2, 3, 4]), 1.0, -5.0)
    meses['soi'] = 0.0
    res = agregar_pacifico_safra(meses).set_index('ano')
    # safra 2020 = set-dez/2019 + jan-abr/2020 -> só meses com oni = 1.0
    assert res.loc[2020, 'oni_medio'] == 1.0

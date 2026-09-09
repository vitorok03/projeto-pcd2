"""Testes das funções de agregação temporal e espacial.
Rode com: pytest tests/
"""
import numpy as np
import pandas as pd
import pytest

from soja_clima.agregacao import agregar_espacial_para_microrregiao, ano_safra, fase_fenologica


def test_ano_safra_antes_de_setembro_fica_no_mesmo_ano():
    assert ano_safra(pd.Timestamp("2024-03-15")) == 2024


def test_ano_safra_a_partir_de_setembro_vai_para_o_ano_seguinte():
    assert ano_safra(pd.Timestamp("2024-09-15")) == 2025


def test_fase_fenologica_cobre_as_4_fases_na_ordem_esperada():
    safra = 2024
    assert fase_fenologica(pd.Timestamp("2023-09-05"), safra) == "plantio"
    assert fase_fenologica(pd.Timestamp("2023-10-20"), safra) == "vegetativo"
    assert fase_fenologica(pd.Timestamp("2023-12-15"), safra) == "floracao_enchimento"
    assert fase_fenologica(pd.Timestamp("2024-02-01"), safra) == "maturacao"


def test_fase_fenologica_fora_da_janela_retorna_none():
    assert fase_fenologica(pd.Timestamp("2023-06-01"), 2024) is None


def test_agregacao_espacial_pondera_por_completude():
    """Duas estações na mesma microrregião: a de maior completude deve
    pesar mais na média ponderada."""
    dados = pd.DataFrame({
        'codigo_estacao': ['E1', 'E2'],
        'code_micro': ['M001', 'M001'],
        'safra': [2020, 2020],
        'prec_total_safra_completa': [400.0, 300.0],
        'temp_max_abs_safra_completa': [35.0, 38.0],
        'completude_safra_completa': [0.95, 0.60],
    })

    resultado = agregar_espacial_para_microrregiao(dados, fases=['safra_completa'])
    linha = resultado.iloc[0]

    esperado = (400.0 * 0.95 + 300.0 * 0.60) / (0.95 + 0.60)
    assert linha['prec_total_safra_completa'] == pytest.approx(esperado)

    # Extremo: max entre as estações, nunca uma média
    assert linha['temp_max_abs_safra_completa'] == 38.0

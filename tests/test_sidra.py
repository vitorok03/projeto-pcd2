import pandas as pd

from soja_clima.sidra import preparar_soja_microrregiao


def test_preparar_soja_microrregiao_converte_numeros_com_virgula_decimal(capsys):
    df = pd.DataFrame({
        'code_micro': ['1101'],
        'name_micro': ['Norte GO'],
        'abbrev_state': ['GO'],
        'Ano': ['2024'],
        'Área plantada (Hectares)': ['85000'],
        'Área colhida (Hectares)': ['85000'],
        'Quantidade produzida (Toneladas)': ['290700'],
        'Rendimento médio da produção (Quilogramas por Hectare)': ['3420'],
    })
    resultado = preparar_soja_microrregiao(df)
    assert resultado['rendimento_kg_ha'].iloc[0] == 3420.0
    assert resultado['area_plantada_ha'].iloc[0] == 85000.0


def test_preparar_soja_microrregiao_trata_valores_ausentes():
    df = pd.DataFrame({
        'code_micro': ['1103'], 'name_micro': ['Leste GO'], 'abbrev_state': ['GO'],
        'Ano': ['2024'],
        'Área plantada (Hectares)': ['-'], 'Área colhida (Hectares)': ['-'],
        'Quantidade produzida (Toneladas)': ['-'],
        'Rendimento médio da produção (Quilogramas por Hectare)': ['-'],
    })
    resultado = preparar_soja_microrregiao(df)
    assert pd.isna(resultado['producao_ton'].iloc[0])

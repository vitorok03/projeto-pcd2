from .inmet import ler_arquivo_inmet, agregar_diario, ler_e_agregar_diario
from .sidra import ler_sidra_soja, agregar_soja_para_microrregiao, preparar_soja_microrregiao
from .agregacao import (
    ano_safra,
    fase_fenologica,
    agregar_diario_para_estacao_safra,
    agregar_espacial_para_microrregiao,
)
from .merge import montar_base_final
from .qualidade import (
    diagnosticar_arquivo,
    filtrar_estacoes_fora_do_brasil,
    detectar_sequencias_repetidas,
    FAIXAS_PLAUSIVEIS,
)

# geo.py não é reexportado aqui porque depende de geopandas/geobr, que
# são pesados e nem todo notebook precisa deles -- importe direto com
# `from soja_clima.geo import construir_mapa_estacao_microrregiao`
# quando for usar o join espacial.

__all__ = [
    "ler_arquivo_inmet", "agregar_diario", "ler_e_agregar_diario",
    "ler_sidra_soja", "agregar_soja_para_microrregiao", "preparar_soja_microrregiao",
    "ano_safra", "fase_fenologica",
    "agregar_diario_para_estacao_safra", "agregar_espacial_para_microrregiao",
    "montar_base_final",
    "diagnosticar_arquivo", "filtrar_estacoes_fora_do_brasil",
    "detectar_sequencias_repetidas", "FAIXAS_PLAUSIVEIS",
]

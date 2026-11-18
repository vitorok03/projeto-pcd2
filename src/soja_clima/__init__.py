# --- API da main (contrato da equipe) -------------------------------------
from .inmet import ler_arquivo_inmet, agregar_diario, ler_e_agregar_diario
from .sidra import ler_sidra_soja, agregar_soja_para_microrregiao, preparar_soja_microrregiao
from .agregacao import (
    ano_safra,
    fase_fenologica,
    agregar_diario_para_estacao_safra,
    agregar_espacial_para_microrregiao,
)
from .merge import (
    montar_base_final,
    agregar_clima_micro_safra,
    agregar_pacifico_safra,
    adicionar_solo,
    selecionar_colunas_solo,
    filtrar_base_modelagem,
    calcular_desvio_clima,
    carregar_base_final,
)
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

# --- Etapas de aquisição do pipeline (notebooks/pipeline/01, 03 e 04) -------
# Esses módulos dependem de rasterio/requests/geobr. Para manter a convenção
# acima (importar o pacote não exige dependências pesadas), eles são
# carregados sob demanda: `from soja_clima import processar_dados_soilgrids`
# só importa `soja_clima.solo` quando o nome é acessado.
# (A soja é lida por `sidra.ler_sidra_soja`, a partir do CSV gerado pela etapa 02.)
_PIPELINES_SOB_DEMANDA = {
    "carregar_e_agregar_inmet": "clima",
    "processar_dados_soilgrids": "solo",
    "processar_indices_noaa": "pacifico",
}


def __getattr__(nome: str) -> object:
    if nome in _PIPELINES_SOB_DEMANDA:
        import importlib
        modulo = importlib.import_module(f".{_PIPELINES_SOB_DEMANDA[nome]}", __name__)
        return getattr(modulo, nome)
    raise AttributeError(f"module {__name__!r} has no attribute {nome!r}")


__all__ = [
    "ler_arquivo_inmet", "agregar_diario", "ler_e_agregar_diario",
    "ler_sidra_soja", "agregar_soja_para_microrregiao", "preparar_soja_microrregiao",
    "ano_safra", "fase_fenologica",
    "agregar_diario_para_estacao_safra", "agregar_espacial_para_microrregiao",
    "montar_base_final", "agregar_clima_micro_safra", "agregar_pacifico_safra",
    "adicionar_solo", "selecionar_colunas_solo", "filtrar_base_modelagem", "calcular_desvio_clima", "carregar_base_final",
    "diagnosticar_arquivo", "filtrar_estacoes_fora_do_brasil",
    "detectar_sequencias_repetidas", "FAIXAS_PLAUSIVEIS",
    *_PIPELINES_SOB_DEMANDA,
]

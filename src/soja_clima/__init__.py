from .clima import processar_dados_inmet
from .soja import processar_dados_sidra
from .solo import processar_dados_soilgrids
from .pacifico import processar_indices_noaa
from .merge import consolidar_base_final

__all__ = [
    "processar_dados_inmet", "processar_dados_sidra", 
    "processar_dados_soilgrids", "processar_indices_noaa", "consolidar_base_final"
]
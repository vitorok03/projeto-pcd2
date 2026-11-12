---
tipo: pipeline
fonte: codigo
tags: [pipeline, solo]
---
# Etapa 03: Processar solo

`notebooks/pipeline/03_processar_solo.ipynb`: rasters do SoilGrids → `solo_microrregioes_limpo.parquet`.

Usa `processar_dados_soilgrids` ([[Módulo solo]]): média zonal por microrregião, uma coluna por raster. A etapa "limpo" fica no notebook (não lida).

Decisão: [[D13 Solo como covariável estática]]. Fonte: [[SoilGrids — solo]]. Análise: [[EDA Solo]]. Riscos: [[Pontos de atenção do código]].

---
tipo: modulo
fonte: codigo
tags: [codigo]
---
# Módulo solo

`src/soja_clima/solo.py`: estatística zonal do SoilGrids por microrregião.

## Função
- `processar_dados_soilgrids(pasta_rasters) -> DataFrame`

## Como funciona
1. Lê as microrregiões do geobr (2020) e cria `CD_MICRO` (`code_micro` → inteiro → texto).
2. Lista os `.tif` da pasta; o nome do arquivo sem a extensão vira a coluna.
3. Para cada raster: lê CRS e valor nodata com `rasterio` (padrão −32768 se ausente), reprojeta as microrregiões para o CRS do raster e chama `rasterstats.zonal_stats(..., stats=['mean'], nodata=...)`.
4. Microrregião sem pixel válido fica `NaN`.
5. Se um raster falhar, imprime um aviso e preenche a coluna com `NaN`, sem interromper.

## Observações
- Os valores ficam na escala original do SoilGrids; não há conversão de unidades.
- Dependências: `rasterio`, `rasterstats`, `geopandas`, `geobr`.
- Risco: falha silenciosa por raster ([[Pontos de atenção do código]]).

Ver [[SoilGrids — solo]] · [[D13 Solo como covariável estática]] · [[Estatística zonal]] · [[CRS]]

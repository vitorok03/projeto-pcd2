---
tipo: modulo
fonte: conversa
tags: [codigo]
---
# Módulo geo

`src/soja_clima/geo.py`: join espacial estação → microrregião (requer geopandas e geobr).

## Funções (conforme a versão das conversas; podem ter mudado)
- `montar_geodataframe_estacoes(diario)`
- `construir_mapa_estacao_microrregiao(diario, microrregioes, distancia_maxima_km)`

`DISTANCIA_MAXIMA_KM = 150`. Dois fallbacks: estação fora de qualquer polígono e microrregião sem estação ([[D06 Distância máxima de 150 km]]). Ver [[Point-in-polygon]] e [[CRS]].

Uso no `main.ipynb`: `construir_mapa_estacao_microrregiao(diario, microrregioes)`, seguido de junção interna do `code_micro` no diário.

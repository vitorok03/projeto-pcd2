---
tipo: glossario
tags: [glossario]
---
# Point-in-polygon

Teste geométrico: o ponto (estação) cai dentro de qual polígono (microrregião)? Implementado por `geopandas.sjoin`. Quando nenhum polígono contém o ponto, usa-se `sjoin_nearest` com limite de distância. Ver [[Módulo geo]].

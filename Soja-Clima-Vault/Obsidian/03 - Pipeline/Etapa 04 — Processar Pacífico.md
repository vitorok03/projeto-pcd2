---
tipo: pipeline
fonte: codigo
tags: [pipeline, pacifico]
---
# Etapa 04: Processar Pacífico

`notebooks/pipeline/04_processar_pacifico.ipynb`: ONI/SOI da NOAA → `pacifico_indices.parquet`.

Usa `processar_indices_noaa` ([[Módulo pacifico]]): baixa o ONI se faltar, lê os dois arquivos por tentativa de formato e entrega `ano, mes, oni, soi`. O valor por safra é calculado depois, no `main` ([[D14 Índices do Pacífico ONI e SOI]]).

Fonte: [[NOAA — ONI e SOI]]. Análise: [[EDA Correlação e Anomalias]]. Questão: [[Q05 Defasagem dos índices ONI e SOI]].

---
tipo: fonte
fonte: codigo
tags: [fonte, solo]
---
# SoilGrids: solo

Rasters (`.tif`) do [SoilGrids](https://soilgrids.org/) em `data/raw/soil/`, resumidos por microrregião em `solo_microrregioes_limpo.parquet` ([[Módulo solo]], [[Etapa 03 — Processar solo]]).

## O que o código faz
- Um raster por variável e profundidade; o nome do arquivo vira o nome da coluna (ex.: `phh2o_0-5cm_mean`)
- [[Estatística zonal]]: **média** dos pixels dentro de cada microrregião, ignorando o valor nodata do raster
- As microrregiões são reprojetadas para o CRS do raster antes do cálculo ([[CRS]])

## O que entra na base final
Sete variáveis da camada 0–5 cm: pH (`phh2o`), argila (`clay`), areia (`sand`), carbono orgânico (`soc`), CTC (`cec`), densidade do solo (`bdod`) e água disponível (`wv0033`). Escalas do SoilGrids mantidas: pH ×10, argila e areia em g/kg, carbono orgânico em dg/kg ([[D13 Solo como covariável estática]]).

## Contexto geral
SoilGrids (ISRIC) é um mapeamento digital global de solo, ~250 m, em várias profundidades.

## A preencher
- [ ] Quais profundidades/variáveis existem em `data/raw/soil/` além de 0–5 cm
- [ ] O que significa "limpo" no nome do parquet (a limpeza não está em `processar_dados_soilgrids`)
- [ ] Quantas microrregiões ficaram sem valor ([[Pontos de atenção do código]])

---
tipo: fonte
fonte: codigo
tags: [fonte, pacifico]
---
# NOAA: ONI e SOI

Arquivos mensais `oni_monthly.txt` e `soi_monthly.txt` em `data/raw/`, tratados em `pacifico_indices.parquet` ([[Módulo pacifico]], [[Etapa 04 — Processar Pacífico]]).

## O que o código faz
- ONI: se o arquivo não existe, baixa de `https://psl.noaa.gov/data/correlation/oni.data`. O SOI **não** é baixado (arquivo manual)
- Tenta quatro formatos em ordem: `AAAAMM,valor` (SOI), linhas `ano v1 ... v12` (ONI), tabela com cabeçalho `JAN..DEC` e três colunas `ano mes valor`
- Valores ≤ −99 são tratados como ausentes
- Resultado: tabela `ano, mes, oni, soi` (junção externa)

## Da série mensal ao valor da safra
`agregar_pacifico_safra` tira a **média de set a abr** e rotula pelo ano da colheita ([[D14 Índices do Pacífico ONI e SOI]]). Sem defasagem ([[Q05 Defasagem dos índices ONI e SOI]]).

## Contexto geral
- [[ONI]]: anomalia da temperatura do mar na região Niño 3.4, média móvel de 3 meses; ±0,5 °C delimita El Niño e La Niña
- [[SOI]]: diferença de pressão entre Taiti e Darwin
- Ambos descrevem o [[ENSO]]

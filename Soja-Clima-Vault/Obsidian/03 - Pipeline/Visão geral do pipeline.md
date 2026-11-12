---
tipo: pipeline
fonte: readme
tags: [pipeline]
---
# Visão geral do pipeline

| Etapa | Entrada | Saída | Módulos |
|---|---|---|---|
| [[Etapa 01 — Processar clima]] | `data/raw/inmet/*.zip` | `data/processed/clima_diario.parquet` | [[Módulo clima]], [[Módulo inmet]], [[Módulo qualidade]] |
| [[Etapa 02 — Processar soja]] | API do SIDRA | `data/raw/tabela1612.csv` | [[Módulo sidra]] |
| [[Etapa 03 — Processar solo]] | `data/raw/soil/` | `data/processed/solo_microrregioes_limpo.parquet` | [[Módulo solo]] |
| [[Etapa 04 — Processar Pacífico]] | `oni_monthly.txt`, `soi_monthly.txt` | `data/processed/pacifico_indices.parquet` | [[Módulo pacifico]] |
| [[main — base final de modelagem]] | tudo acima | `data/processed/base_final_modelagem.csv` | [[Módulo geo]], [[Módulo agregacao]], [[Módulo merge]] |

Ordem de execução: as quatro etapas de `notebooks/pipeline/` (independentes entre si) e depois o `main.ipynb`.

Princípios: [[D09 Agregar cedo, em streaming]] · [[D10 Pacote src e notebooks]]

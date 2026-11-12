---
tipo: decisao
id: D10
status: ativa
fonte: readme
criado: 2026-11-10
tags: [decisao]
---
# D10: Pacote src e notebooks


## Contexto
Funções coladas em vários notebooks/células duplicavam correções (cada novo formato do INMET exigia editar vários lugares).

## Decisão
`src/soja_clima/` guarda só definições; `notebooks/` e `main.ipynb` orquestram. Etapas independentes salvam parquet intermediário. Saída do Colab para execução local.

Relacionado: [[Estrutura do repositório]] · [[O que mudou desde a versão anterior]] · [[P10 Google Drive lento no Colab]]

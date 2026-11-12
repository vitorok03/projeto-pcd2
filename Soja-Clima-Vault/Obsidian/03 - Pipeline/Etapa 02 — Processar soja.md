---
tipo: pipeline
fonte: readme
tags: [pipeline, soja]
---
# Etapa 02: Processar soja

`notebooks/pipeline/02_processar_soja.ipynb`: API do SIDRA (Tabela 1612) → `data/raw/tabela1612.csv`.

O `main.ipynb` lê esse CSV com `ler_sidra_soja`, ou seja, como tabela **municipal**.

Pontos de atenção herdados: [[P06 Rodapé do SIDRA e skipfooter]] (se ainda ler CSV com rodapé), [[P04 Colisão de nome na chave de junção]] e [[D11 Chave de junção nunca é só o nome]] (ao ligar ao geobr), [[D12 Só microrregiões produtoras]].

Fonte: [[SIDRA — Tabela 1612]]. Código: [[Módulo sidra]].

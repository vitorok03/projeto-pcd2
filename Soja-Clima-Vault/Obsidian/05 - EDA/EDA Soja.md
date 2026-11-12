---
tipo: eda
fonte: conversa
notebook: notebooks/eda/eda_soja.ipynb
tags: [eda, soja]
---
# EDA Soja

Notebook: `notebooks/eda/eda_soja.ipynb`.

## Achados já registrados
- 558 microrregiões no Brasil, mas só ~334 produzem soja em algum ano ([[P07 Denominador de 558 microrregiões]])
- Produção municipal de 2024 somada: ~144,5 milhões de toneladas (arquivo usado nos testes)
- Mais da metade dos municípios não planta soja (`-` não é erro) ([[SIDRA — Tabela 1612]])

- Os filtros da base de modelagem vêm desta EDA: área colhida ≥ 100 ha e rendimento ≤ 6.000 kg/ha ([[D16 Filtros da base de modelagem]])

## Checklist
- [ ] Distribuição de rendimento e produção, outliers
- [ ] Tendência do rendimento por ano (nacional e por região): [[D15 Tendência tecnológica e detrending]]
- [ ] Anos de histórico por microrregião (lacunas)
- [ ] Rendimento × área plantada
- [ ] Mapa da produção/rendimento

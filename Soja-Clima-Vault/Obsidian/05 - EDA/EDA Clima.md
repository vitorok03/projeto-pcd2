---
tipo: eda
fonte: conversa
notebook: notebooks/eda/eda_clima_horario_diario.ipynb
tags: [eda, clima]
---
# EDA Clima

Notebook: `notebooks/eda/eda_clima_horario_diario.ipynb`.

## Achados já registrados
- Rede de estações cresce de 63 (2005) a ~590 (2018) ([[Limitações conhecidas]])
- Temperatura mínima de −51 °C no diário: era a [[P02 Estação da Antártica]]
- A401 (BA) com 45 °C repetidos em 21–23/06/2007: [[P03 Sensor travado]]
- Precipitação máxima diária de ~415 mm no PA em 2019: extremo plausível na Amazônia, mas conferir
- 548 de 614 estações com coordenadas levemente divergentes entre anos: benigno ([[P08 Coordenadas divergentes e índice duplicado]])

- Esses alertas viraram os limites do `main`: ver [[D17 Limites físicos dos sensores]] (o código os chama "Alerta 6 da EDA")

## Checklist
- [ ] Completude por estação × ano · [ ] gaps · [ ] distribuições · [ ] sazonalidade por mês · [ ] correlação entre variáveis · [ ] outliers

Fonte: [[INMET — estações automáticas]]

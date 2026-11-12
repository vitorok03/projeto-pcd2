---
tipo: decisao
id: D17
status: ativa
fonte: codigo
criado: 2026-11-10
tags: [decisao]
---
# D17: Limites físicos dos sensores


## Decisão
Remover dias fisicamente implausíveis, vindos do "Alerta 6 da EDA":
- `temp_min >= -10`
- `prec_total <= 300` mm/dia
- `gdd <= 35`

Aplicados no `main` (etapa 1) e, opcionalmente, em `agregar_clima_micro_safra` (que o `main` chama com `aplicar_limites_fisicos=False` para não repetir).

## Consequências
O dia inteiro é descartado (todas as variáveis), mesmo que só uma falhe. O limite de 300 mm também remove eventos reais raros ([[Pontos de atenção do código]]).

Relacionado: [[P02 Estação da Antártica]] · [[P03 Sensor travado]] · [[Módulo merge]] · [[EDA Clima]]

---
tipo: decisao
id: D12
status: ativa
fonte: codigo
criado: 2026-11-10
tags: [decisao]
---
# D12: Só microrregiões produtoras


## Decisão original
Filtrar `producao_ton > 0` **antes** do merge final. O `how='outer'` com a malha do geobr mantinha as 558 microrregiões, produzindo soja ou não.

## Como está no código
O `main` não tem esse filtro isolado. A exclusão acontece em `filtrar_base_modelagem`: `area_colhida_ha >= 100` remove áreas pequenas **e** as sem soja (valor ausente não passa na condição). É mais restritivo que `producao_ton > 0` ([[D16 Filtros da base de modelagem]]).

## Consequências
Estatísticas de cobertura devem usar como denominador as microrregiões que **passam** nesse filtro. Resultado do ajuste antigo: 329 de 334 microrregiões produtoras na base final.

Relacionado: [[P07 Denominador de 558 microrregiões]] · [[Q01 Microrregiões produtoras fora da base final]]

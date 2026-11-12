---
tipo: problema
id: P07
status: resolvido
fonte: conversa
tags: [problema]
---
# P07: Denominador de 558 microrregiões


**Sintoma:** "553 de 558 microrregiões com soja restaram na base final", número que não podia ser verdade.

**Causa:** o `how='outer'` com a malha do geobr mantinha todas as 558 microrregiões, produzindo soja ou não; `nunique()` contava todas. O `inner join` final também deixava passar linhas com produção `NaN`.

**Correção:** filtrar `producao_ton > 0` antes do merge ([[D12 Só microrregiões produtoras]]). Novo resultado: 329 de 334.

**Prevenção:** conferir o que o denominador realmente representa.

Relacionado: [[Q01 Microrregiões produtoras fora da base final]]

---
tipo: problema
id: P06
status: resolvido
fonte: conversa
tags: [problema]
---
# P06: Rodapé do SIDRA e skipfooter


**Sintoma:** o último município (Brasília) sumia; 9 linhas de dado perdidas.

**Causa:** `skipfooter` conta linhas lógicas do parser, e as notas do rodapé têm campos com quebra de linha entre aspas. Além disso, procurar a linha que começa com `"Fonte` dava falso positivo no município **Fonte Boa (AM)**.

**Correção:** localizar a linha que começa com `"Fonte:` e cortar o texto manualmente antes de passar ao `read_csv` (via `StringIO`).

Relacionado: [[Módulo sidra]] · [[SIDRA — Tabela 1612]]

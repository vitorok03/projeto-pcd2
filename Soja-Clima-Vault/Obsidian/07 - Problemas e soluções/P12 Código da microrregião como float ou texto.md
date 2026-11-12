---
tipo: problema
id: P12
status: resolvido
fonte: conversa
tags: [problema]
---
# P12: Código da microrregião como float ou texto


**Sintoma:** `code_micro` aparecia como `13009.0` (float) em partes do pipeline e como texto em outras; os merges podiam não casar.

**Correção:** `_padronizar_cd_micro` transforma `'5101.0'`, `5101.0` e `'5101'` em `'5101'`. `CD_MICRO` (texto) é usado em solo, clima e base final, e `carregar_base_final` lê o CSV com `dtype=str` nessa coluna.

**Prevenção:** padronizar a chave logo na entrada de cada fonte e conferir o `dtype` antes de cada merge.

Relacionado: [[Q01 Microrregiões produtoras fora da base final]] · [[Módulo merge]]

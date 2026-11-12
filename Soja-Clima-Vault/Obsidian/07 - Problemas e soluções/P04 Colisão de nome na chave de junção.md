---
tipo: problema
id: P04
status: resolvido
fonte: conversa
tags: [problema]
---
# P04: Colisão de nome na chave de junção


**Sintoma:** `groupby(['code_micro','ano']).size()` com valores > 1 (160 combinações duplicadas; 122 grupos com 2 linhas na base final).

**Causa:** a chave usava só o nome da microrregião e descartava a UF. Nomes iguais em estados diferentes viraram produto cartesiano no merge, **misturando a produção de uma microrregião com a de outra**.

**Correção:** extrair a UF para uma coluna e montar `nome_casefold + '_' + uf`; mesmo formato do lado do geobr (`name_micro` + `abbrev_state`).

**Prevenção:** [[D11 Chave de junção nunca é só o nome]]; checar duplicidade depois de todo merge.

Relacionado: [[Chave de junção]] · [[P07 Denominador de 558 microrregiões]]

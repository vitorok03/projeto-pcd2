---
tipo: decisao
id: D11
status: ativa
fonte: conversa
criado: 2026-11-10
tags: [decisao]
---
# D11: Chave de junção nunca é só o nome


## Decisão
Preferir `code_micro`. Quando só há nome: normalizar (`casefold`, sem espaços extras) **e incluir a UF** (`nome_uf`). Depois de todo merge, checar duplicidade de `(code_micro, ano)`.

## Origem
[[P04 Colisão de nome na chave de junção]] (nomes repetidos entre estados) e a divergência de capitalização (`Espírito-santense` × `Espírito-Santense`).

Relacionado: [[Chave de junção]] · [[geobr — microrregiões]]

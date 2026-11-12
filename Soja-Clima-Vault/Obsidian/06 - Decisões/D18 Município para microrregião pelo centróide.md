---
tipo: decisao
id: D18
status: ativa
fonte: codigo
criado: 2026-11-10
tags: [decisao]
---
# D18: Município para microrregião pelo centróide


## Contexto
O SIDRA usado no `main` é municipal; a produção precisa chegar à microrregião.

## Decisão (etapa 2 do `main`)
1. Baixa os municípios e as microrregiões do geobr (2020)
2. Troca cada município pelo seu **centróide** e faz `sjoin(predicate="within")` com as microrregiões
3. Liga ao SIDRA por **nome do município normalizado** (minúsculas, sem acentos) **+ UF**
4. Soma entre municípios e recalcula o rendimento (`agregar_soja_para_microrregiao`)

## Consequências
A junção é interna: municípios sem correspondência de nome somem sem aviso. O centróide pode cair em outra microrregião em formas côncavas ([[Pontos de atenção do código]]).

Relacionado: [[D11 Chave de junção nunca é só o nome]] · [[Módulo sidra]] · [[Chave de junção]]

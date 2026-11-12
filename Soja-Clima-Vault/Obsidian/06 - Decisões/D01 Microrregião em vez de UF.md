---
tipo: decisao
id: D01
status: ativa
fonte: conversa
criado: 2026-11-10
tags: [decisao]
---
# D01: Microrregião em vez de UF


## Contexto
O SIDRA entrega produção por área administrativa e por ano; as estações do INMET são pontos esparsos.

## Opções
- **UF inteira:** simples e robusto a uma estação ruim, mas estados grandes (MT, GO, BA) têm clima heterogêneo. A média apaga a variação que explica diferença de produtividade e atenua o coeficiente do clima (erro de medição).
- **Município + estação mais próxima:** granular, mas ~5,5 mil municípios para poucas estações geram blocos repetidos e ruído de distância.
- **Microrregião:** meio-termo, unidade oficial do IBGE, o SIDRA exporta nesse nível e dá para usar [[Point-in-polygon]].

## Decisão
Microrregião (558 no Brasil).

## Consequências
Microrregiões sem estação dependem de substituta ([[D06 Distância máxima de 150 km]]); algumas produtoras ficam sem clima ([[Q01 Microrregiões produtoras fora da base final]]).

Relacionado: [[Microrregião]] · [[geobr — microrregiões]] · [[D11 Chave de junção nunca é só o nome]]

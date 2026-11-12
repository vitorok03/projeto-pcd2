---
tipo: fonte
fonte: conversa
tags: [fonte, geo]
---
# geobr: microrregiões

`geobr.read_micro_region(year=2020)` devolve a malha oficial do IBGE: 558 microrregiões.

- Colunas: `code_micro`, `name_micro`, `code_state`, `abbrev_state`, `name_state`, `code_region`, `name_region`, `year`, `geometry`
- CRS de origem: EPSG:4674 (SIRGAS 2000)
- Baixa do servidor do IBGE a cada chamada (precisa de internet)

Usos: ponte entre o nome/código do SIDRA e o polígono ([[Chave de junção]]) e destino do [[Point-in-polygon]] das estações ([[Módulo geo]]).

Ver [[Microrregião]], [[D01 Microrregião em vez de UF]], [[D11 Chave de junção nunca é só o nome]]

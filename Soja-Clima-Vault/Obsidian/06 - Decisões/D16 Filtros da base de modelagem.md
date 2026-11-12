---
tipo: decisao
id: D16
status: ativa
fonte: codigo
criado: 2026-11-10
tags: [decisao]
---
# D16: Filtros da base de modelagem


## Decisão
`filtrar_base_modelagem(area_min_ha=100, rendimento_max_kg_ha=6000, ano_min=2009)`, com filtros vindos da EDA. Cada filtro imprime quantas linhas remove.

| Filtro | Motivo (do código) |
|---|---|
| `area_colhida_ha >= 100` | ruído de áreas pequenas; remove também microrregiões sem soja |
| `rendimento_kg_ha <= 6000` | rendimento fisicamente plausível para soja comercial |
| `ano >= 2009` | antes disso, mais de 25% do clima ausente ([[Q04 Recorte temporal inicial]]) |

## Consequências
Muda a coorte: refazer as contagens de cobertura ([[Q01 Microrregiões produtoras fora da base final]]).

Relacionado: [[D12 Só microrregiões produtoras]] · [[Módulo merge]] · [[EDA Soja]]

---
tipo: decisao
id: D05
status: ativa
fonte: conversa
criado: 2026-11-10
tags: [decisao]
---
# D05: Agregação temporal e espacial


## Contexto
Há duas agregações diferentes, com regras diferentes por tipo de variável.

| Tipo | Temporal (dentro da estação) | Espacial (entre estações) |
|---|---|---|
| Soma/contagem (chuva, dias secos, GDD) | soma | **média** (ponderada por completude no desenho original) |
| Média (temp., umidade) | média | média |
| Extremo (temp. máx./mín.) | max/min | max/min |

## Decisão
Somar chuva de várias estações multiplicaria o total pelo número de estações; o correto é a média entre pontos. Extremos nunca viram média.

O README confirma "soma por estação e média entre estações" e a docstring do `merge.py` confirma a **média ponderada pela completude** (extremos max/min). A versão anterior da refatoração somava entre estações e inflou os totais: [[P11 Soma entre estações multiplicava a chuva]].

Relacionado: [[Módulo agregacao]] · [[Q03 Ponderação por completude foi mantida]]

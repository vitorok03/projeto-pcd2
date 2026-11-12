---
tipo: decisao
id: D14
status: ativa
fonte: codigo
criado: 2026-11-10
tags: [decisao]
---
# D14: Índices do Pacífico ONI e SOI


## O que o código faz
- `agregar_pacifico_safra`: média de ONI e SOI nos meses **set a abr** (`MESES_SAFRA`), rotulada pelo ano da colheita (set–dez contam para o ano seguinte)
- Gera `oni_medio` e `soi_medio`, **um valor por ano**, juntados por `ano` (`left join`)
- **Sem defasagem**

## Consequências
- O valor é igual para todas as microrregiões do ano: só varia no tempo, e fica colinear com um efeito de ano
- Usa informação até abril da própria safra: serve para explicar, não para prever antes do fim da safra ([[Q05 Defasagem dos índices ONI e SOI]])
- Combina com `desvio_clima`, que também é um valor por ano ([[Pontos de atenção do código]])

## Contexto geral
O [[ENSO]] modula a chuva no Brasil (em geral mais chuva no Sul em El Niño e seca no Norte/Nordeste; padrão oposto em La Niña).

Relacionado: [[NOAA — ONI e SOI]] · [[Módulo pacifico]] · [[Módulo merge]]

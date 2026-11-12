---
tipo: decisao
id: D04
status: ativa
fonte: conversa
criado: 2026-11-10
tags: [decisao]
---
# D04: Limiar de completude de 80 por cento


## Contexto
`sum()` e `mean()` ignoram dias faltantes sem avisar: uma estação com 60% dos dias dá uma soma subestimada que parece plausível.

## Decisão
- [[Completude]] = dias válidos ÷ dias esperados no período; um dia só é válido com ≥ 18 horas
- Abaixo de 80%, as estatísticas da estação-safra viram `NaN`
- A completude **viaja como metadado/peso**, não como feature (não tem relação causal com produtividade)
- Soma de chuva não é normalizada pela completude (chuva é "espicada", o gap pode ter sido o dia mais chuvoso)

## Consequências
Extremos (máx./mín.) podem subestimar o valor real mesmo com 99% de completude.

Relacionado: [[Módulo agregacao]] · [[Q03 Ponderação por completude foi mantida]] · [[Q04 Recorte temporal inicial]]

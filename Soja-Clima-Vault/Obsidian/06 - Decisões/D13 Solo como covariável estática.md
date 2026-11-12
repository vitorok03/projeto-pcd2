---
tipo: decisao
id: D13
status: ativa
fonte: codigo
criado: 2026-11-10
tags: [decisao]
---
# D13: Solo como covariável estática


## O que o código faz
- Média zonal de cada raster por microrregião ([[Módulo solo]])
- Mantém **7 variáveis da camada 0–5 cm**: pH, argila, areia, carbono orgânico, CTC, densidade e água disponível (`selecionar_colunas_solo`)
- Descarta as outras profundidades para reduzir a multicolinearidade entre camadas. O silte também fica de fora; como argila + areia + silte somam ~1000 g/kg, manter os três seria colinear (leitura nossa: o código só cita colinearidade entre camadas)
- Entra na base por `left join` em `CD_MICRO`: uma linha por microrregião, constante no tempo

## Consequência
Solo não varia no tempo. Num modelo com [[Efeito fixo]] por microrregião, ele fica colinear com o efeito fixo; é útil em modelos sem efeito fixo, mistos ou para explicar diferenças de nível entre regiões.

## A preencher
- [ ] Por que só 0–5 cm · [ ] como entra no modelo · [ ] interação com clima

Relacionado: [[SoilGrids — solo]] · [[Módulo merge]]

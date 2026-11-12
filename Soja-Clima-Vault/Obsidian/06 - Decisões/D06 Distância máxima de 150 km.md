---
tipo: decisao
id: D06
status: ativa
fonte: conversa
criado: 2026-11-10
tags: [decisao]
---
# D06: Distância máxima de 150 km


## Contexto
O join espacial deixa estações sem polígono e microrregiões sem estação. O fallback "mais próxima" não tem sentido físico a qualquer distância.

## Decisão
`DISTANCIA_MAXIMA_KM = 150` nos dois fallbacks (estação → microrregião mais próxima; microrregião vazia → estação mais próxima do centróide). Além disso, caixa geográfica do Brasil (lat −34 a 6, lon −74 a −32) para descartar estações fora do país.

## Consequências
Casos de Antártica e ilhas oceânicas ficam de fora ([[P02 Estação da Antártica]]). O valor de 150 km foi um chute razoável: revisar olhando a distribuição real das distâncias.

Relacionado: [[Módulo geo]] · [[CRS]] · [[Q01 Microrregiões produtoras fora da base final]]

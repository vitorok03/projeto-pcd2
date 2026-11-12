---
tipo: fonte
fonte: conversa
tags: [fonte, clima]
---
# INMET: estações automáticas

Portal: https://portal.inmet.gov.br/dadoshistoricos. Um arquivo por estação e ano, com uma linha por hora.

## Formato do arquivo (CSV)
- 8 linhas de metadados (região, UF, estação, código WMO, latitude, longitude, altitude, data de fundação), depois o cabeçalho das colunas
- Encoding `latin1`, separador `;`, decimal com vírgula, `;` final gera coluna fantasma
- `-9999` = dado ausente
- Radiação noturna vem como `-9999` mas significa 0 (heurística: fora de 09h–19h UTC)

## Variáveis usadas
Precipitação horária, temperatura (ar, máx. e mín. na hora), umidade relativa, radiação global, velocidade do vento.

## Volume e cobertura
- Cerca de 9 mil arquivos estação-ano, de 2005 a 2024
- Estações ativas: 63 em 2005, pico de ~590 em 2018, ~451 em 2021 e ~541 em 2024
- Poucas estações em alguns estados (DF 5, AP 4, RR 3)

## Armadilhas
[[P01 Formato do INMET muda entre anos]] · [[P02 Estação da Antártica]] · [[P03 Sensor travado]] · [[P08 Coordenadas divergentes e índice duplicado]] · [[Q02 Arquivos de 2005 com formato diferente]]

Código: [[Módulo inmet]] · [[Módulo clima]] · [[Módulo qualidade]]. Etapa: [[Etapa 01 — Processar clima]]

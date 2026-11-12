---
tipo: problema
id: P03
status: resolvido
fonte: conversa
tags: [problema]
---
# P03: Sensor travado


**Sintoma:** estação A401 (BA) com `temp_max = 45,0 °C` em 21, 22 e 23/06/2007, em pleno inverno.

**Causa provável:** sensor saturado/travado. O filtro de faixa não pega (45 está no limite superior, não acima).

**Correção:** `detectar_sequencias_repetidas` aponta candidatos; o julgamento é humano (valores repetidos plausíveis, como 25,3 °C por 3 dias, são coincidência). Exclusões registradas em `exclusoes_manuais.csv` (estação, início, fim, motivo), aplicadas ao montar o diário. O CSV funciona como documentação versionável da limpeza.

Relacionado: [[Módulo qualidade]] · [[Etapa 01 — Processar clima]]

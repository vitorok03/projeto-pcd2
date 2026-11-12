---
tipo: problema
id: P02
status: resolvido
fonte: conversa
tags: [problema]
---
# P02: Estação da Antártica


**Sintoma:** temperatura mínima de −51 °C e "estação mais fria do Brasil" com média de −31 °C.

**Causa:** a estação `C891 CRIOSFERA` (Estação Antártica Comandante Ferraz) tem `UF: SP` no cabeçalho, mas coordenadas −84/−79. Entrava em todas as estatísticas nacionais.

**Correção:** `filtrar_estacoes_fora_do_brasil` (caixa lat −34..6, lon −74..−32) já na construção do diário; limite de 150 km também a barra no join espacial ([[D06 Distância máxima de 150 km]]).

**Prevenção:** nunca confiar na UF do cabeçalho; validar coordenadas.

Relacionado: [[Módulo qualidade]] · [[EDA Clima]]

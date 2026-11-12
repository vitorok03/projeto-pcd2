---
tipo: problema
id: P11
status: resolvido
fonte: conversa
tags: [problema]
---
# P11: Soma entre estações multiplicava a chuva


**Sintoma:** valores impossíveis na base, como 13.764 mm de chuva por ano e 2.985 dias secos num ano (exemplos citados na docstring do `merge.py`).

**Causa:** a versão anterior da refatoração somava todos os dias de todas as estações da microrregião. A soma ficava multiplicada pelo número de estações (precipitação, GDD e dias secos).

**Correção:** o clima passa sempre pela agregação de `agregacao.py`: soma no tempo **dentro** de cada estação, depois média ponderada **entre** estações; extremos por max/min. `agregar_clima_micro_safra` reaproveita as mesmas funções.

**Prevenção:** [[D05 Agregação temporal e espacial]]. Conferir a ordem de grandeza (chuva da safra costuma ficar entre ~500 e ~3.000 mm).

Relacionado: [[Módulo merge]] · [[O que mudou desde a versão anterior]]

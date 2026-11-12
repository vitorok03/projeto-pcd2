---
tipo: questao
id: Q03
status: resolvida
fonte: codigo
tags: [questao]
---
# Q03: Ponderação por completude foi mantida


## Pergunta
A média entre estações ainda é ponderada pela [[Completude]]?

## Resposta
Sim, segundo a docstring de `merge.py`: agregação espacial por **média ponderada pela completude**, com extremos por max/min. Ficou pendente conferir o código atual de `agregacao.py` (não lido), mas o `main` usa `agregar_espacial_para_microrregiao` sem alterá-la.

Relacionado: [[D05 Agregação temporal e espacial]] · [[P11 Soma entre estações multiplicava a chuva]] · [[Módulo merge]]

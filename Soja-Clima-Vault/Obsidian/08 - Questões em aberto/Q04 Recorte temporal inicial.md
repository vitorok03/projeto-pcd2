---
tipo: questao
id: Q04
status: resolvida
fonte: codigo
tags: [questao]
---
# Q04: Recorte temporal inicial


## Pergunta
Vale começar a base de modelagem em ~2009 em vez de 2005?

## Resposta
Sim: `filtrar_base_modelagem(ano_min=2009)`, com a justificativa no código de que antes de 2009 mais de 25% do clima fica ausente ([[D16 Filtros da base de modelagem]]).

## Ainda vale checar
Mapear a % de linhas com clima válido e a distância média da estação usada por safra, para confirmar que 2009 é o corte certo ([[Limitações conhecidas]]).

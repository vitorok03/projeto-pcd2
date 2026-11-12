---
tipo: questao
id: Q02
status: aberta
fonte: conversa
tags: [questao]
---
# Q02: Arquivos de 2005 com formato diferente


## Pergunta
Por que os arquivos de 2005 falham?

## Contexto
Erro em `INMET_NE_BA_A406_CRUZ DAS ALMAS_..._2005.CSV`: `'str' object has no attribute 'groupby'`. O caminho também tem `2005\2005\` aninhado (pasta duplicada).

## Hipótese
Cabeçalho com número de linhas de metadado diferente de 8 (o `skiprows=8` desalinha e a primeira linha de dado vira cabeçalho).

## Como testar
Imprimir as 12 primeiras linhas do arquivo com `repr(linha)` e ajustar o parser, como em [[P01 Formato do INMET muda entre anos]].

## Verificar
Se o novo [[Módulo clima]] (leitura de ZIPs) já resolveu isso.

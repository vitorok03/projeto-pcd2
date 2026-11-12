---
tipo: questao
id: Q05
status: aberta
fonte: codigo
tags: [questao]
---
# Q05: Defasagem dos índices ONI e SOI


## Pergunta
Para o objetivo do trabalho, a média de set a abr da mesma safra basta, ou é preciso usar os índices com antecedência?

## Contexto
O código usa a média de set a abr da safra, **sem defasagem** ([[D14 Índices do Pacífico ONI e SOI]]). Isso explica bem a safra, mas só fica disponível no fim dela. Se o objetivo for **prever** antes ou durante o plantio, o índice precisa de meses anteriores (ex.: jun–ago).

## Como testar
Gerar variantes com janelas anteriores e comparar correlações e desempenho; decidir primeiro se o trabalho é explicativo ou preditivo ([[Pergunta de pesquisa]]).

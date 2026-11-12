---
tipo: questao
id: Q06
status: investigando
fonte: codigo
tags: [questao]
---
# Q06: Método de detrending


## Pergunta
O detrending atual introduz vazamento de informação?

## Contexto
Método conhecido: polinômio de grau 2 sobre o rendimento **nacional** ponderado por área; `desvio_clima` = série − tendência, o mesmo valor para todas as microrregiões do ano ([[D15 Tendência tecnológica e detrending]]).

## Hipóteses de risco
- A tendência usa todos os anos, inclusive os que forem teste
- O rendimento nacional do ano contém o alvo da microrregião
- Um valor por ano fica colinear com efeitos de ano e com ONI/SOI

## Como testar
Ajustar a tendência só com os anos de treino e comparar resultados; confirmar se `desvio_clima` entra como feature ou no alvo; comparar com tendência por microrregião. Ver [[Pontos de atenção do código]].

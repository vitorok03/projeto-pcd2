---
tipo: decisao
id: D15
status: ativa
fonte: codigo
criado: 2026-11-10
tags: [decisao]
---
# D15: Tendência tecnológica e detrending


## Contexto
O rendimento da soja sobe ano a ano por melhoria genética e de manejo, independente do clima. Sem tratar isso, o modelo confunde "ano recente" com "clima favorável".

## O que o código faz (`calcular_desvio_clima`, grau 2)
1. Calcula o **rendimento nacional** de cada ano, ponderado pela área: Σ produção × 1000 ÷ Σ área colhida
2. Ajusta um **polinômio de grau 2** a essa série (anos centralizados)
3. Cria `rendimento_tendencia` (valor do polinômio) e `desvio_clima` = rendimento nacional − tendência
4. Junta por `ano`: **o mesmo valor para todas as microrregiões do ano**

A interpretação é que o desvio da série nacional em relação à tendência reflete o clima do ano.

## Cuidados
Ajuste com todos os anos, e uso do rendimento do próprio ano, abrem risco de vazamento. Detalhes em [[Pontos de atenção do código]] e [[Q06 Método de detrending]].

## A confirmar
Se `desvio_clima` é feature ou parte do alvo, e se a modelagem também usa lag do rendimento.

Relacionado: [[Detrending]] · [[Módulo merge]] · [[D03 Alvo é o rendimento]]

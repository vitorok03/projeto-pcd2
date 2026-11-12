---
tipo: decisao
id: D08
status: ativa
fonte: a-confirmar
criado: 2026-11-10
tags: [decisao]
---
# D08: Validação temporal e baselines


## Contexto
Os dados são um painel (microrregião × ano). Embaralhar linhas vaza o futuro para o treino.

## Decisão (desenho das conversas)
- Corte **temporal** (ex.: percentil 80 dos anos como início do teste), nunca aleatório
- Baseline de [[Persistência (baseline)]]
- Regressão regularizada com [[Efeito fixo]] de microrregião + lag do rendimento + clima
- Random Forest/Gradient Boosting depois, desconfiando de amostras pequenas
- Modelo misto (`MixedLM`) como alternativa se houver pouco histórico por microrregião
- Métricas em kg/ha (MAE, RMSE), sempre comparadas ao baseline

## A confirmar
O que de fato foi implementado: [[Q07 Modelos e resultados]].

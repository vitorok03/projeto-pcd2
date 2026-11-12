---
tipo: decisao
id: D09
status: ativa
fonte: conversa
criado: 2026-11-10
tags: [decisao]
---
# D09: Agregar cedo, em streaming


## Contexto
Milhares de arquivos horários somam dezenas de milhões de linhas.

## Decisão
Ler um arquivo, agregar para diário, **descartar o horário** e acumular só os diários (~24× menores). Cada arquivo com tratamento de erro próprio; falhas viram uma lista no fim, não interrompem o processamento.

Relacionado: [[Etapa 01 — Processar clima]] · [[Módulo inmet]]

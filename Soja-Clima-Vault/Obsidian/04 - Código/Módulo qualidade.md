---
tipo: modulo
fonte: conversa
tags: [codigo]
---
# Módulo qualidade

`src/soja_clima/qualidade.py`: diagnósticos de qualidade dos dados climáticos.

## Funções (conforme a versão das conversas; podem ter mudado)
- `diagnosticar_arquivo(path)`
- `filtrar_estacoes_fora_do_brasil(df, coluna_lat, coluna_lon)`
- `detectar_sequencias_repetidas(df, coluna, min_repeticoes)`
- `FAIXAS_PLAUSIVEIS, BRASIL_LAT, BRASIL_LON`

Ver [[P02 Estação da Antártica]] e [[P03 Sensor travado]]. O detector aponta candidatos; a decisão de excluir é humana. O filtro de Brasil é usado no `main` e em `merge.agregar_clima_micro_safra`.

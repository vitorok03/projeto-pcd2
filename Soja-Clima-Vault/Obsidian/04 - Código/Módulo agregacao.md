---
tipo: modulo
fonte: conversa
tags: [codigo]
---
# Módulo agregacao

`src/soja_clima/agregacao.py`: diário → estação-safra → microrregião-safra.

## Funções (conforme a versão das conversas; podem ter mudado)
- `ano_safra(data)`
- `fase_fenologica(data, safra)`
- `agregar_diario_para_estacao_safra(df, usar_fases)`
- `agregar_espacial_para_microrregiao(df, fases)`
- `DIAS_ESPERADOS_FASE, LIMIAR_COMPLETUDE`

Ver [[D02 Ano-safra de setembro a agosto]], [[D04 Limiar de completude de 80 por cento]], [[D05 Agregação temporal e espacial]], [[D07 Fases fenológicas]].

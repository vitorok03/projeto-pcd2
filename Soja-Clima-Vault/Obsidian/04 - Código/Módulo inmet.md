---
tipo: modulo
fonte: conversa
tags: [codigo]
---
# Módulo inmet

`src/soja_clima/inmet.py`: leitura e limpeza dos arquivos horários do INMET.

## Funções (conforme a versão das conversas; podem ter mudado)
- `ler_arquivo_inmet(path)`
- `normalizar_chave_meta(chave)`
- `agregar_diario(df_horario)`
- `ler_e_agregar_diario(path)`
- `COLUNAS_CONHECIDAS, COLUNAS_ESSENCIAIS`

Trata [[P01 Formato do INMET muda entre anos]]. Usado na [[Etapa 01 — Processar clima]].

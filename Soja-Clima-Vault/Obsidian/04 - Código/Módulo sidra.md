---
tipo: modulo
fonte: conversa
tags: [codigo]
---
# Módulo sidra

`src/soja_clima/sidra.py`: leitura e preparação da produção de soja do SIDRA.

## Funções (conforme a versão das conversas; podem ter mudado)
- `ler_sidra_soja(path)`
- `agregar_soja_para_microrregiao(df)`
- `preparar_soja_microrregiao(df)`

Uso no `main.ipynb`: `ler_sidra_soja` + `agregar_soja_para_microrregiao` (caminho municipal). `preparar_soja_microrregiao` não é usada no `main`. Ver [[P06 Rodapé do SIDRA e skipfooter]], [[P07 Denominador de 558 microrregiões]] e [[D18 Município para microrregião pelo centróide]].

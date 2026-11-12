---
tipo: pipeline
fonte: readme
tags: [pipeline, clima]
---
# Etapa 01: Processar clima

`notebooks/pipeline/01_processar_clima.ipynb`: ZIPs do INMET → `clima_diario.parquet`.

## O que a lógica precisa garantir (do histórico do projeto)
- Leitura resiliente a mudanças de formato ([[P01 Formato do INMET muda entre anos]])
- Hora → dia **arquivo por arquivo**, sem juntar o horário ([[D09 Agregar cedo, em streaming]])
- Dia só vale com pelo menos 18 horas válidas
- Variáveis diárias: precipitação total, temp. média/máx./mín., umidade, radiação, vento, amplitude, dia seco (< 1 mm), [[GDD]]
- Lista de arquivos sem duplicar ([[P05 glob duplica arquivos no Windows]])

## O que o `main.ipynb` revela sobre a saída
- O parquet usa `VL_LATITUDE` e `VL_LONGITUDE`; o `main` renomeia para `latitude` e `longitude`
- Tem as colunas `temp_min`, `prec_total` e `gdd`, usadas nos limites físicos ([[D17 Limites físicos dos sensores]])
- Estações fora do Brasil são removidas já no `main` ([[P02 Estação da Antártica]])

## A confirmar
Como o `clima.py` abre os ZIPs e quais proteções foram portadas ([[Módulo clima]]). Pendência: [[Q02 Arquivos de 2005 com formato diferente]].

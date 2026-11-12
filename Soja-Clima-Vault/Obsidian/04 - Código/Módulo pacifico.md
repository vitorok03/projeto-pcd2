---
tipo: modulo
fonte: codigo
tags: [codigo]
---
# Módulo pacifico

`src/soja_clima/pacifico.py`: leitura e limpeza dos índices ONI e SOI da NOAA.

## Funções
- `baixar_oni(caminho_destino)`: baixa `https://psl.noaa.gov/data/correlation/oni.data`
- `ler_e_limpar_noaa(caminho_arquivo, nome_indice)`: tenta quatro parsers, na ordem: `AAAAMM,valor` (SOI), `ano v1..v12` (ONI), tabela `JAN..DEC`, três colunas `ano mes valor`; imprime linhas `[debug]` com tamanho e primeiras linhas
- `processar_indices_noaa(caminho_oni, caminho_soi)`: baixa o ONI se o arquivo não existir; devolve `ano, mes, oni, soi` (junção externa, ordenada)

## Regras de limpeza
Valores ≤ −99 viram ausentes e são descartados; anos fora de 1900–2100 e meses fora de 1–12 são ignorados.

## Observações
- O SOI precisa estar em `data/raw/` (não é baixado).
- A conversão para valor por safra **não** está aqui: está em `merge.agregar_pacifico_safra` ([[Módulo merge]]).

Ver [[NOAA — ONI e SOI]] · [[D14 Índices do Pacífico ONI e SOI]] · [[ONI]] · [[SOI]]

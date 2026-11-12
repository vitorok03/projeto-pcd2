---
tipo: revisao
fonte: codigo
tags: [codigo, riscos]
---
# Pontos de atenção do código

Revisão feita lendo `solo.py`, `pacifico.py`, `merge.py` e `main.ipynb`. Nada disso foi executado: são riscos a conferir, do mais importante ao menos importante.

## 1. Detrending pode vazar informação (`calcular_desvio_clima`)
- A tendência (polinômio de grau 2) é ajustada com **todos** os anos. Se a base for dividida por tempo, os anos de teste já influenciaram a tendência.
- `desvio_clima` usa o rendimento **nacional do próprio ano**, que inclui a microrregião-alvo. Como feature para prever o rendimento da microrregião, é quase vazamento do alvo.
- É um valor **único por ano**: não distingue efeito-ano e fica correlacionado com `oni_medio` e `soi_medio` (também um valor por ano).
- Sugestão: decidir se é alvo (rendimento − tendência) ou feature; estimar a tendência só com os anos de treino. Ver [[Q06 Método de detrending]].

## 2. Limites físicos removem o dia inteiro (`LIMITES_FISICOS`)
`prec_total_max = 300` elimina todas as variáveis do dia, inclusive eventos reais (a EDA viu ~415 mm/dia no PA em 2019). Sugestão: contar dias removidos por regra e por UF; considerar sinalizar em vez de descartar. Ver [[D17 Limites físicos dos sensores]].

## 3. Junção município–SIDRA por nome é interna e silenciosa
No `main`, `merge(..., how="inner")` descarta sem avisar municípios cujo nome normalizado não casa (apóstrofos como D'Oeste, grafias, renomeações). Sugestão: comparar a soma de `producao_ton` e o número de municípios antes e depois, e listar os não casados (`indicator=True`). Ver [[D18 Município para microrregião pelo centróide]].

## 4. `solo.py` esconde falhas
Qualquer exceção vira coluna `NaN`. Sugestão: checar `df.isna().mean()` por coluna e falhar acima de um limite.

## 5. Pacífico sem defasagem e com informação da própria safra
Média de set a abr da mesma safra: serve para explicar, mas não para prever antes do fim da safra. Ver [[Q05 Defasagem dos índices ONI e SOI]].

## 6. `n_dias_validos` é aproximado
`completude média × 241`; `taxa_chuva_diaria`, `fracao_dias_secos` e `gdd_medio_diario` herdam a aproximação.

## 7. Centróide do município
Em municípios de forma côncava o centróide pode cair em outra microrregião; `representative_point()` evita isso. Além disso, o centróide em coordenadas geográficas gera aviso: projetar antes (ex.: EPSG:5880).

## 8. A coorte mudou
Área ≥ 100 ha e ano ≥ 2009 mudam quais microrregiões entram. Refazer a conta de [[Q01 Microrregiões produtoras fora da base final]] depois dos filtros.

## 9. Imports
O `main` usa `from src.soja_clima...`; o README manda instalar com `pip install -e .`. Padronizar para os notebooks de outras pastas.

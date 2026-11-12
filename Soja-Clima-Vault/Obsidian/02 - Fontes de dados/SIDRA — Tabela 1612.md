---
tipo: fonte
fonte: conversa
tags: [fonte, soja]
---
# SIDRA: Tabela 1612

IBGE, Produção Agrícola Municipal (lavouras temporárias). Filtro: soja (em grão).

## Variáveis
Área plantada (ha), área colhida (ha), quantidade produzida (t), rendimento médio (kg/ha).

## Formato do CSV exportado
- Linhas 1–2: título e cabeçalho truncado; linha 3: cabeçalho real; rodapé com "Fonte:", notas e legenda
- BOM UTF-8 (`utf-8-sig`), separador `;`, aspas, decimal com vírgula
- `-` marca ausência (a cultura não existe no local); `..`, `...` e `X` aparecem na legenda
- Nome da unidade vem como `Nome (UF)`
- O "ano" é o ano da colheita (premissa a conferir na metodologia da PAM; ver [[D02 Ano-safra de setembro a agosto]])

## Níveis de exportação já usados
Município (um arquivo por ano) e microrregião (série 2005–2024). Hoje a [[Etapa 02 — Processar soja]] baixa pela API e o `main.ipynb` lê `data/raw/tabela1612.csv` com `ler_sidra_soja`, ou seja, **nível município**; a microrregião é montada depois ([[D18 Município para microrregião pelo centróide]]).

## Armadilhas
[[P06 Rodapé do SIDRA e skipfooter]] · [[P04 Colisão de nome na chave de junção]] · [[P07 Denominador de 558 microrregiões]]

Código: [[Módulo sidra]]

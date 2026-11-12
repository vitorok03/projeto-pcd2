---
tipo: modulo
fonte: codigo
tags: [codigo]
---
# Módulo merge

`src/soja_clima/merge.py`: merge final, filtros, solo, Pacífico e detrending da base de modelagem. Orquestrado pelo [[main — base final de modelagem]].

## Princípio documentado no módulo
O clima usa **sempre** a agregação de `agregacao.py`:
1. temporal, dentro de cada estação, na janela da safra (1º de setembro do ano anterior + 240 dias, rotulada pelo ano da colheita, o mesmo `ano` do PAM/SIDRA), com limiar de completude;
2. espacial, entre as estações da microrregião, por **média ponderada** pela completude (extremos = max/min).

Por que: [[P11 Soma entre estações multiplicava a chuva]].

## Constantes
- `DIAS_JANELA_SAFRA = 241`; `MESES_SAFRA = [9,10,11,12,1,2,3,4]`
- `LIMITES_FISICOS = {temp_min_min: -10, prec_total_max: 300, gdd_max: 35}` ([[D17 Limites físicos dos sensores]])
- `SOLO_COLUNAS_MANTER`: 7 variáveis de 0–5 cm ([[D13 Solo como covariável estática]])

## Funções
| Função | O que faz |
|---|---|
| `montar_base_final(clima, producao)` | junção interna por `code_micro` e `ano` = `safra` |
| `agregar_clima_micro_safra(clima, mapa, aplicar_limites_fisicos)` | clima + mapa estação–microrregião → uma linha por microrregião-safra (safra inteira, `usar_fases=False`); renomeia colunas para os nomes legados; cria `n_dias_validos = completude × 241` e as taxas por dia |
| `agregar_pacifico_safra(pacifico, meses)` | média de ONI e SOI nos meses set–abr por ano-safra ([[D14 Índices do Pacífico ONI e SOI]]) |
| `adicionar_solo(base, solo)` | `left join` por `CD_MICRO` (texto) |
| `selecionar_colunas_solo(base)` | descarta camadas redundantes, mantém as 7 de 0–5 cm |
| `filtrar_base_modelagem(base, area_min_ha=100, rendimento_max_kg_ha=6000, ano_min=2009)` | filtros da EDA, imprime quantas linhas cada um remove ([[D16 Filtros da base de modelagem]]) |
| `calcular_desvio_clima(base, grau=2)` | detrending ([[D15 Tendência tecnológica e detrending]]) |
| `carregar_base_final(caminho, nomes_eda, descartar)` | lê o CSV final com `CD_MICRO` texto; renomeia colunas de soja para os nomes dos notebooks de EDA |
| `_padronizar_cd_micro(serie)` | `'5101.0'`, `5101.0` e `'5101'` viram `'5101'` ([[P12 Código da microrregião como float ou texto]]) |

## Mapeamento para os notebooks de EDA (`NOMES_EDA`)
`producao_ton → quantidade_produzida`, `area_colhida_ha → área_colhida`, `area_plantada_ha → área_plantada`, `rendimento_kg_ha → rendimento_recalculado`.

Riscos: [[Pontos de atenção do código]].

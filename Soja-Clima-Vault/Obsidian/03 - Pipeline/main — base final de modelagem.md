---
tipo: pipeline
fonte: codigo
tags: [pipeline, base-final]
---
# main: base final de modelagem

`main.ipynb` (raiz). Gera `data/processed/base_final_modelagem.csv`, a única base final. Caminho base: `PCD2_BASE_DIR` ou diretório atual.

## As 8 etapas do notebook
| # | O que faz | Detalhe |
|---|---|---|
| 1 | Clima diário | lê `clima_diario.parquet`; renomeia `VL_LATITUDE/VL_LONGITUDE`; remove estações fora do Brasil ([[P02 Estação da Antártica]]); aplica limites físicos ([[D17 Limites físicos dos sensores]]) |
| 2 | Soja | `ler_sidra_soja` (municipal) → centróide do município nas microrregiões do geobr → junção por nome normalizado + UF → `agregar_soja_para_microrregiao` ([[D18 Município para microrregião pelo centróide]], [[D11 Chave de junção nunca é só o nome]]) |
| 3 | Estação → microrregião | `construir_mapa_estacao_microrregiao` + junção interna com o diário ([[D06 Distância máxima de 150 km]]) |
| 4 | Clima no tempo | `agregar_diario_para_estacao_safra(usar_fases=True)` |
| 5 | Clima no espaço | `agregar_espacial_para_microrregiao` (fases) + `agregar_clima_micro_safra` (safra completa) + `agregar_pacifico_safra` ([[D05 Agregação temporal e espacial]], [[D07 Fases fenológicas]], [[D14 Índices do Pacífico ONI e SOI]]) |
| 6 | Merge | `montar_base_final` (junção interna) + solo + nome da microrregião + safra completa + Pacífico; **`assert` de que `(code_micro, ano)` é único** ([[P04 Colisão de nome na chave de junção]]) |
| 7 | Filtros | `filtrar_base_modelagem`, `selecionar_colunas_solo`, `calcular_desvio_clima` ([[D16 Filtros da base de modelagem]], [[D13 Solo como covariável estática]], [[D15 Tendência tecnológica e detrending]]) |
| 8 | Exporta | CSV |

## Colunas da base final (deduzidas do código)
- Identificação: `code_micro`, `CD_MICRO` (texto), `NM_MICRO`, `ano`, `safra`
- Soja: `area_plantada_ha`, `area_colhida_ha`, `producao_ton`, `n_municipios`, `rendimento_kg_ha`
- Clima por fase: `<estatística>_<fase>` (plantio, vegetativo, floracao_enchimento, maturacao) e `completude_<fase>`, mais `n_estacoes`
- Clima da safra inteira: `precipitacao_total`, `dias_secos_total`, `temp_media_anual`, `temp_max_anual`, `temp_min_anual`, `gdd_total`, `amplitude_media`, `radiacao_media`, `completude`, `n_dias_validos`, `taxa_chuva_diaria`, `fracao_dias_secos`, `gdd_medio_diario` (os nomes dizem "anual", mas são da **safra**)
- Solo (0–5 cm): `phh2o`, `clay`, `sand`, `soc`, `cec`, `bdod`, `wv0033`
- Pacífico: `oni_medio`, `soi_medio`
- Tendência: `rendimento_tendencia`, `desvio_clima`

## Checklist de validação
- [x] `(code_micro, ano)` único: garantido por `assert`
- [ ] Quantas microrregiões produtoras restaram e quais saíram: [[Q01 Microrregiões produtoras fora da base final]]
- [ ] Distribuição de [[Completude]] concentrada perto de 1
- [ ] Clima plausível (chuva da safra, ordem de grandeza: [[P11 Soma entre estações multiplicava a chuva]]) e rendimento entre ~1.500 e 6.000 kg/ha
- [ ] Soma da produção municipal antes e depois da junção por nome ([[Pontos de atenção do código]])
- [ ] Contagem por `origem` do mapa estação–microrregião (própria × substituta)
- [ ] Faltantes por coluna de solo

Riscos conhecidos: [[Pontos de atenção do código]].

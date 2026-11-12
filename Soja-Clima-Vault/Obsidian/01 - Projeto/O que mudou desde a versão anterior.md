---
tipo: projeto
fonte: readme
tags: [projeto, historico]
---
# O que mudou desde a versão anterior

Comparação entre o desenho que construímos nas conversas (scripts de Colab e depois o pacote local) e o README atual.

| Tema | Antes | Agora (README) |
|---|---|---|
| Ambiente | Colab + Google Drive ([[P10 Google Drive lento no Colab]]) | Local, repositório Git ([[D10 Pacote src e notebooks]]) |
| Entrada INMET | CSVs soltos por estação-ano | ZIPs anuais em `data/raw/inmet/` ([[Módulo clima]]) |
| Soja | CSV exportado à mão do SIDRA | Baixado pela API na [[Etapa 02 — Processar soja]] |
| Notebooks | `01_eda_horaria`, `02_uniao_climatica`... numerados | `notebooks/pipeline/01..04`, `notebooks/eda/` e `main.ipynb` orquestrador |
| Agregação do clima | Safra completa, sem fases (por ora) | **Fases fenológicas + safra completa** ([[D07 Fases fenológicas]]) |
| Agregação espacial | Média ponderada por completude | Mantida: soma no tempo por estação, **média ponderada** entre estações; extremos max/min ([[Q03 Ponderação por completude foi mantida]]) |
| Dados novos | Só clima (INMET) | **Solo** ([[SoilGrids — solo]]) e **Pacífico** ([[NOAA — ONI e SOI]]) |
| Merge | `montar_base_final` | Merge + filtros, solo e **detrending** ([[Módulo merge]], [[D15 Tendência tecnológica e detrending]]) |
| Base final | `base_final_microrregiao.parquet` | `base_final_modelagem.csv` |
| Soja | Exportação por microrregião ou município, ligada por nome | Tabela municipal; município → microrregião pelo **centróide** do município e nome normalizado + UF ([[D18 Município para microrregião pelo centróide]]) |
| Filtros | Só limiar de completude | Limites físicos dos sensores e filtros da base de modelagem ([[D17 Limites físicos dos sensores]], [[D16 Filtros da base de modelagem]]) |
| Relatórios | Nenhum | Dois scripts geram HTML a partir dos notebooks ([[Relatórios HTML de EDA]]) |

## Histórico da refatoração
O `merge.py` cita uma "refatoração" anterior, com `05_merge_final` e `correcoes_filtros`, cujas etapas foram incorporadas ao `main.ipynb` (marcadas `[ACRÉSCIMO]`). Aquela versão **somava todos os dias de todas as estações** da microrregião, multiplicando chuva, GDD e dias secos: [[P11 Soma entre estações multiplicava a chuva]]. Hoje o clima usa sempre a agregação de `agregacao.py`.

---
tipo: eda
fonte: readme
tags: [eda, relatorios]
---
# Relatórios HTML de EDA

Dois scripts na raiz leem os notebooks (`.ipynb`) e montam um HTML único com textos Markdown, código e gráficos PNG embutidos em base64:

| Script | Lê | Gera |
|---|---|---|
| `gerar_documento_eda.py` | os 4 notebooks de `notebooks/eda/` | `documento_eda_completo.html` |
| `gerar_relatorio_projeto.py` | `notebooks/eda`, `notebooks/pipeline` e a raiz (5 notebooks, incluindo Feature Engineering) | `relatorio_completo_projeto.html` |

Mapeamento dos notebooks: `eda_clima_horario_diario` ([[EDA Clima]]), `eda_soja` ([[EDA Soja]]), `eda_solo` ([[EDA Solo]]), `eda_correlacao_anomalias` ([[EDA Correlação e Anomalias]]), `06_feature_engineering_e_insights` ([[Feature Engineering e Clusters]]).

Uso: o HTML serve de material para a apresentação. Células Markdown dos notebooks viram os blocos "[Análise]", então vale escrever as conclusões lá.

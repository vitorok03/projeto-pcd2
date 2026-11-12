---
tipo: projeto
fonte: readme
tags: [projeto, repositorio]
---
# Estrutura do repositório

Fonte: README de [https://github.com/vitorok03/projeto-pcd2](https://github.com/vitorok03/projeto-pcd2).

```
projeto-pcd2/
├── src/soja_clima/        # lógica reutilizável (só definições)
│   ├── inmet.py           # leitura e limpeza dos CSV horários do INMET
│   ├── clima.py           # leitura dos ZIPs do INMET e agregação para diário
│   ├── sidra.py           # leitura e preparação da produção de soja
│   ├── geo.py             # join espacial estação → microrregião
│   ├── agregacao.py       # diário → estação-safra → microrregião-safra
│   ├── solo.py            # estatística zonal do SoilGrids por microrregião
│   ├── pacifico.py        # índices ONI/SOI (NOAA)
│   ├── merge.py           # merge final + filtros, solo e detrending
│   └── qualidade.py       # diagnósticos de qualidade
├── notebooks/
│   ├── pipeline/          # etapas 01 a 04 (aquisição e processamento)
│   └── eda/               # análises exploratórias (leem a base final)
├── main.ipynb             # orquestrador: gera a base final única
├── tests/                 # testes das funções de src/
├── data/                  # bruto e processado (não versionado)
├── gerar_documento_eda.py       # HTML a partir dos notebooks de EDA
├── gerar_relatorio_projeto.py   # HTML completo (EDA + pipeline)
├── pyproject.toml · requirements.txt · README.md · .gitignore
```

## Dados brutos esperados (`data/raw/`)
- `inmet/`: ZIPs anuais do INMET
- `soil/`: rasters do SoilGrids
- `oni_monthly.txt` e `soi_monthly.txt` (NOAA; o ONI é baixado automaticamente se faltar)
- `tabela1612.csv`: gerado pela [[Etapa 02 — Processar soja]]

## Como o `main.ipynb` importa
`from src.soja_clima.<módulo> import ...`: roda a partir da **raiz do repositório**. O caminho base vem de `PCD2_BASE_DIR` (variável de ambiente) ou do diretório atual. Os módulos usam imports relativos (`from .agregacao import ...`), então funcionam também instalados como `soja_clima` (`pip install -e .`).

Navegação: [[Visão geral do pipeline]] · [[Módulo inmet]] · [[Módulo clima]] · [[Módulo sidra]] · [[Módulo geo]] · [[Módulo agregacao]] · [[Módulo solo]] · [[Módulo pacifico]] · [[Módulo merge]] · [[Módulo qualidade]]

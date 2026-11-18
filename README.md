# soja-clima

Previsão de produção de soja no Brasil a partir de dados climáticos do
INMET (estações automáticas) e produção agrícola do SIDRA (Tabela 1612).

## Estrutura

```
src/soja_clima/   # lógica reutilizável (sem execução, só definições)
  inmet.py        # leitura de um CSV horário do INMET (diagnóstico/análise)
  clima.py        # leitura dos ZIPs do INMET e agregação para diário
  sidra.py        # leitura e preparação da produção de soja (SIDRA)
  geo.py          # join espacial estação -> microrregião (requer geopandas/geobr)
  agregacao.py    # diário -> estação-safra -> microrregião-safra
  solo.py         # estatística zonal do SoilGrids por microrregião
  pacifico.py     # índices ONI/SOI (NOAA)
  merge.py        # merge final + filtros, solo e detrending da base de modelagem
  qualidade.py    # diagnósticos: faixas plausíveis, gaps, sequências repetidas

notebooks/pipeline/  # etapas de aquisição/processamento (01 a 04)
notebooks/eda/       # análises exploratórias (leem a base final)
notebooks/legado/    # notebooks antigos, fora do pipeline oficial (só referência)
main.ipynb           # orquestrador: gera a base final única
tests/               # testes das funções de src/
data/                # dados brutos e processados (não versionado, ver .gitignore)
```

## Instalação

```bash
pip install -e ".[pipeline,eda,dev]"   # pacote soja_clima + extras dos notebooks e testes
```

Os notebooks importam o pacote diretamente (`from soja_clima.merge import ...`),
sem `sys.path`. O `requirements.txt` continua disponível como alternativa.

## Pipeline (ordem de execução)

1. `notebooks/pipeline/01_processar_clima.ipynb` — ZIPs do INMET → `data/processed/clima_diario.parquet`
2. `notebooks/pipeline/02_processar_soja.ipynb` — API do SIDRA (Tabela 1612) → `data/raw/tabela1612.csv`
3. `notebooks/pipeline/03_processar_solo.ipynb` — rasters do SoilGrids → `data/processed/solo_microrregioes_limpo.parquet`
4. `notebooks/pipeline/04_processar_pacifico.ipynb` — ONI/SOI da NOAA → `data/processed/pacifico_indices.parquet`
5. `main.ipynb` (na raiz) — mapeamento estação → microrregião, agregação do clima por safra
   (fases fenológicas + safra completa; soma por estação e média entre estações), merge com
   soja, solo e Pacífico, filtros e detrending → **`data/processed/base_final_modelagem.csv`**,
   a única base final do projeto.

## Dados

Os arquivos brutos não são versionados: ZIPs anuais do
[INMET](https://portal.inmet.gov.br/dadoshistoricos) em `data/raw/inmet/`,
rasters do [SoilGrids](https://soilgrids.org/) em `data/raw/soil/` e
`oni_monthly.txt`/`soi_monthly.txt` da [NOAA](https://psl.noaa.gov/data/climateindices/)
em `data/raw/` (o ONI é baixado automaticamente se faltar). A Tabela 1612 do
[SIDRA/IBGE](https://sidra.ibge.gov.br/tabela/1612) é baixada pela etapa 02.

## Testes

```bash
pytest tests/
```

## Limitações conhecidas

- A cobertura de estações do INMET cresce bastante ao longo do tempo
  (poucas estações antes de ~2009) -- safras mais antigas têm mais
  linhas descartadas por baixa completude.
- Algumas microrregiões não têm nenhuma estação dentro delas; o clima
  atribuído nesses casos vem de uma estação substituta (ver coluna
  `origem` no mapa estação-microrregião), com um limiar de distância
  máxima de 150km.

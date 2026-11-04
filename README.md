# soja-clima

Previsão de produção de soja no Brasil a partir de dados climáticos do
INMET (estações automáticas) e produção agrícola do SIDRA (Tabela 1612).

## Estrutura

```
src/soja_clima/   # lógica reutilizável (sem execução, só definições)
  inmet.py        # leitura e limpeza dos arquivos horários do INMET
  sidra.py        # leitura e preparação da produção de soja (SIDRA)
  geo.py          # join espacial estação -> microrregião (requer geopandas/geobr)
  agregacao.py    # diário -> estação-safra -> microrregião-safra
  merge.py        # merge final clima + produção
  qualidade.py    # diagnósticos: faixas plausíveis, gaps, sequências repetidas

notebooks/        # orquestração e exploração (usam o pacote acima)
tests/            # testes das funções de src/
data/             # dados brutos e processados (não versionado, ver .gitignore)
```

## Instalação

```bash
pip install -e .
```

## Pipeline (ordem de execução)

1. `notebooks/01_analise_exploratoria.ipynb` - análise exploratória dos dados climáticos
2. `notebooks/02_agregacao_diaria.ipynb` - agregação dos dados climáticos para granularidade diária
3. `notebooks/03agragacao_inmet_sidra.ipynb` união dos dados climáticos (INMET) e da soja (SIDRA)

## Dados

Os arquivos brutos (CSVs do INMET, um por estação/ano; CSV do SIDRA) não
são versionados. Baixe do [INMET](https://bdmep.inmet.gov.br/) e do
[SIDRA/IBGE](https://sidra.ibge.gov.br/tabela/1612) e coloque em
`data/raw/`.

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

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

1. `notebooks/01_uniao_climatica.ipynb` — lê e agrega os arquivos do INMET (hora -> dia)
2. `notebooks/02_eda_horaria.ipynb` / `03_eda_diaria.ipynb` — diagnóstico de qualidade
3. `notebooks/04_soja_sidra_geobr.ipynb` — leitura do SIDRA + join com microrregiões (geobr)
4. `notebooks/05_join_espacial_microrregioes.ipynb` — estações -> microrregiões
5. `notebooks/06_agregacao_e_merge_final.ipynb` — agregação temporal/espacial + merge final
6. `notebooks/07_validacao_base_final.ipynb` — checagens de sanidade da base final

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

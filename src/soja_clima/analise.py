import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from soja_clima.inmet import ler_arquivo_inmet

GEOJSON_URL = (
    "https://raw.githubusercontent.com/codeforamerica/click_that_hood/"
    "master/public/data/brazil-states.geojson"
)


def mapa_estacoes_animado(
    arquivo,
    col_estado="UF",
    col_ano="ANO",
    col_estacao="CODIGO_ESTACAO",
    ano_inicio=2005,
    ano_fim=2024,
    salvar_html=None,
):
    """
    Gera um mapa choropleth animado (com slider de ano) da quantidade de
    estações INMET por estado.

    Parâmetros
    ----------
    caminho_arquivo : str
        Caminho do CSV com uma linha por estação/ano.
    col_estado : str
        Nome da coluna com a sigla do estado (UF).
    col_ano : str
        Nome da coluna com o ano.
    col_estacao : str
        Nome da coluna que identifica unicamente a estação.
    sep : str
        Separador do CSV.
    ano_inicio, ano_fim : int
        Intervalo de anos a incluir no slider (inclusive).
    salvar_html : str ou None
        Se informado, salva a figura nesse caminho (ex: "mapa.html").

    Retorna
    -------
    plotly.graph_objects.Figure
    """
    # 1. Baixar geojson dos estados do Brasil
    geojson = requests.get(GEOJSON_URL).json()

    # 2. Carregar e filtrar o intervalo de anos
    df = arquivo
    df_filtrado = df[(df[col_ano] >= ano_inicio) & (df[col_ano] <= ano_fim)]

    # 3. Contar estações únicas por estado e por ano
    contagem = (
        df_filtrado
        .groupby([col_estado, col_ano])[col_estacao]
        .nunique()
        .reset_index(name="qtd_estacoes")
    )

    # 4. Garantir grade completa estado x ano (preenche com 0 onde faltar)
    todos_estados = sorted(contagem[col_estado].unique())
    todos_anos = list(range(ano_inicio, ano_fim + 1))
    grade_completa = pd.MultiIndex.from_product(
        [todos_estados, todos_anos], names=[col_estado, col_ano]
    ).to_frame(index=False)
    contagem = grade_completa.merge(contagem, on=[col_estado, col_ano], how="left")
    contagem["qtd_estacoes"] = contagem["qtd_estacoes"].fillna(0).astype(int)

    # 5. Montar o mapa animado
    zmax = contagem["qtd_estacoes"].max()

    fig = px.choropleth(
        contagem,
        geojson=geojson,
        featureidkey="properties.sigla",
        locations=col_estado,
        color="qtd_estacoes",
        animation_frame=col_ano,
        color_continuous_scale="YlOrRd",
        range_color=(0, zmax),
        labels={"qtd_estacoes": "Qtd. estações"},
        title=f"Quantidade de estações INMET por estado ({ano_inicio}–{ano_fim})",
    )

    fig.update_geos(
        visible=True,
        showland=True,
        landcolor="lightgrey",
        showcountries=True,
        countrycolor="white",
        showcoastlines=False,
        scope="south america",
        center={"lat": -14, "lon": -55},
        lataxis_range=[-34, 6],
        lonaxis_range=[-75, -32],
    )

    fig.update_layout(height=650, width=650)

    if salvar_html:
        fig.write_html(salvar_html)

    return fig

def plotar_serie_horaria(path, variavel='temperatura'):
    df = ler_arquivo_inmet(path)
    df = df.sort_values('data')
    timestamp = pd.to_datetime(df['data'].astype(str) + ' ' + df['hora'].astype(str).str.slice(0, 2))

    plt.figure(figsize=(14, 4))
    plt.plot(timestamp, df[variavel], linewidth=0.5)
    plt.title(f"{variavel} — {df['estacao'].iloc[0]} ({df['codigo_estacao'].iloc[0]})")
    plt.xlabel('Data/hora')
    plt.ylabel(variavel)
    plt.tight_layout()
    plt.show()
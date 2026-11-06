import pandas as pd
import numpy as np
import io
import requests
import os

def baixar_oni(caminho_destino: str) -> str:
    url = "https://psl.noaa.gov/data/correlation/oni.data"
    print(f"Baixando ONI de {url}...")
    resposta = requests.get(url, timeout=30)
    resposta.raise_for_status()
    with open(caminho_destino, 'w', encoding='utf-8') as f:
        f.write(resposta.text)
    print(f"Arquivo salvo em {caminho_destino}")
    return caminho_destino

def _tentar_formato_tokens(texto: str, nome_indice: str) -> pd.DataFrame | None:
    """Formato ONI: linhas com 'ano v1 v2 ... v12'. Processa linha por linha."""
    registros = []
    for linha in texto.splitlines():
        partes = linha.split()
        if len(partes) < 13:
            continue
        try:
            ano = int(partes[0])
        except ValueError:
            continue
        if ano < 1900 or ano > 2100:
            continue
        try:
            valores = [float(p) for p in partes[1:13]]
        except ValueError:
            continue
        
        for mes, valor in enumerate(valores, start=1):
            if valor <= -99.0:
                valor = np.nan
            if not np.isnan(valor):
                registros.append([ano, mes, valor])

    if not registros:
        return None
    return pd.DataFrame(registros, columns=['ano', 'mes', nome_indice])

def _tentar_formato_aaaamm_virgula(texto: str, nome_indice: str) -> pd.DataFrame | None:
    """Formato SOI: AAAAMM,valor."""
    registros = []
    for linha in texto.splitlines():
        linha = linha.strip()
        if not linha or ',' not in linha:
            continue
        partes = linha.split(',')
        if len(partes) < 2:
            continue
        try:
            aaaamm = int(partes[0].strip())
            valor = float(partes[1].strip())
        except (ValueError, IndexError):
            continue
        ano = aaaamm // 100
        mes = aaaamm % 100
        if ano < 1900 or ano > 2100 or mes < 1 or mes > 12:
            continue
        if valor <= -99.0:
            valor = np.nan
        if not np.isnan(valor):
            registros.append([ano, mes, valor])

    if not registros:
        return None
    return pd.DataFrame(registros, columns=['ano', 'mes', nome_indice])

def _tentar_formato_tabular(texto: str, nome_indice: str) -> pd.DataFrame | None:
    linhas = texto.splitlines()
    header_idx = -1
    for i, linha in enumerate(linhas):
        if 'JAN' in linha.upper() and 'FEB' in linha.upper():
            header_idx = i
            break
    if header_idx == -1:
        return None
    try:
        df_raw = pd.read_csv(io.StringIO("\n".join(linhas[header_idx:])), sep=r'\s+', engine='python')
    except Exception:
        return None
    col_ano = df_raw.columns[0]
    meses_validos = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
    colunas_meses = [c for c in df_raw.columns if c.upper() in meses_validos]
    if not colunas_meses:
        return None
    df_melt = df_raw.melt(id_vars=[col_ano], value_vars=colunas_meses, var_name='mes_nome', value_name=nome_indice)
    df_melt = df_melt.rename(columns={col_ano: 'ano'})
    meses_map = {m: i + 1 for i, m in enumerate(meses_validos)}
    df_melt['mes'] = df_melt['mes_nome'].str.upper().map(meses_map)
    df_melt[nome_indice] = pd.to_numeric(df_melt[nome_indice], errors='coerce')
    df_melt = df_melt.dropna(subset=['ano', 'mes', nome_indice])
    df_melt['ano'] = df_melt['ano'].astype(int)
    return df_melt[['ano', 'mes', nome_indice]]

def _tentar_formato_3_colunas(texto: str, nome_indice: str) -> pd.DataFrame | None:
    registros = []
    for linha in texto.splitlines():
        linha = linha.strip()
        if not linha or linha.startswith('#'):
            continue
        partes = linha.split()
        if len(partes) < 3:
            continue
        try:
            ano = int(float(partes[0]))
            mes = int(float(partes[1]))
            valor = float(partes[2])
        except (ValueError, IndexError):
            continue
        if ano < 1900 or ano > 2100 or mes < 1 or mes > 12:
            continue
        if valor <= -99.0:
            valor = np.nan
        if not np.isnan(valor):
            registros.append([ano, mes, valor])
    if not registros:
        return None
    return pd.DataFrame(registros, columns=['ano', 'mes', nome_indice])

def ler_e_limpar_noaa(caminho_arquivo: str, nome_indice: str) -> pd.DataFrame:
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        texto = f.read()

    # Diagnóstico: mostra o tamanho e as primeiras linhas não vazias
    print(f"  [debug] {caminho_arquivo}: {len(texto)} caracteres")
    primeiras = [l for l in texto.splitlines() if l.strip()][:3]
    for l in primeiras:
        print(f"  [debug]   {l[:80]}")

    # Tentativa 1: AAAAMM,valor (SOI)
    df = _tentar_formato_aaaamm_virgula(texto, nome_indice)
    if df is not None and len(df) > 0:
        return df

    # Tentativa 2: tokens por linha (ONI)
    df = _tentar_formato_tokens(texto, nome_indice)
    if df is not None and len(df) > 0:
        return df

    # Tentativa 3: tabular com meses
    df = _tentar_formato_tabular(texto, nome_indice)
    if df is not None and len(df) > 0:
        return df

    # Tentativa 4: 3 colunas
    df = _tentar_formato_3_colunas(texto, nome_indice)
    if df is not None and len(df) > 0:
        return df

    raise ValueError(f"Não foi possível identificar o formato de {caminho_arquivo}")

def processar_indices_noaa(caminho_oni: str, caminho_soi: str) -> pd.DataFrame:
    if not os.path.exists(caminho_oni):
        caminho_oni = baixar_oni(caminho_oni)

    print("Processando ONI...")
    df_oni = ler_e_limpar_noaa(caminho_oni, 'oni')
    print(f"  -> {len(df_oni)} registros (de {df_oni['ano'].min()} a {df_oni['ano'].max()})")

    print("Processando SOI...")
    df_soi = ler_e_limpar_noaa(caminho_soi, 'soi')
    print(f"  -> {len(df_soi)} registros (de {df_soi['ano'].min()} a {df_soi['ano'].max()})")

    df_pacifico = pd.merge(df_oni, df_soi, on=['ano', 'mes'], how='outer')
    return df_pacifico.sort_values(['ano', 'mes']).reset_index(drop=True)
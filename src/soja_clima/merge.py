import pandas as pd
import numpy as np

def consolidar_base_final(df_clima: pd.DataFrame, df_soja: pd.DataFrame, df_solo: pd.DataFrame, df_pacifico: pd.DataFrame, df_mapa: pd.DataFrame) -> pd.DataFrame:
    """Realiza o merge de todas as bases na granularidade Microrregião-Safra (Anual)."""
    
    print("Padronizando chaves de integração...")
    
    # PADRONIZAÇÃO ROBUSTA: Remove nulos e converte para string limpa (sem ".0")
    for nome, df in [('soja', df_soja), ('solo', df_solo), ('mapa', df_mapa)]:
        antes = len(df)
        # Remove linhas onde CD_MICRO é nulo
        df.dropna(subset=['CD_MICRO'], inplace=True)
        depois = len(df)
        if antes != depois:
            print(f"  - {nome}: removidas {antes - depois} linhas com CD_MICRO nulo")
        
        # Converte para string e remove o ".0" do final (caso venha como float)
        df['CD_MICRO'] = df['CD_MICRO'].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
    
    df_clima['ano'] = df_clima['ano'].astype(int)
    df_soja['ano'] = df_soja['ano'].astype(int)
    
    # 1. Juntar Clima (diário) com o Mapa (estação -> microrregião)
    # É AQUI que o clima vai se multiplicar para as microrregiões vazias (o que é correto!)
    print("Cruzando Clima com o Mapa de Microrregiões...")
    df_clima_micro = pd.merge(df_clima, df_mapa[['codigo_estacao', 'CD_MICRO']], on='codigo_estacao', how='inner')
    
    # 2. Juntar com o Pacífico (mensal)
    print("Cruzando Clima e Pacífico...")
    df_clima_pacifico = pd.merge(df_clima_micro, df_pacifico, on=['ano', 'mes'], how='left')
    
    # 3. Agregar Clima para nível Anual/Safra por Microrregião
    print("Agregando clima diário para anual...")
    df_clima_anual = df_clima_pacifico.groupby(['CD_MICRO', 'ano']).agg(
        precipitacao_total=('prec_total', 'sum'),
        temp_media_anual=('temp_media', 'mean'),
        temp_max_anual=('temp_max', 'max'),
        temp_min_anual=('temp_min', 'min'),
        gdd_total=('gdd', 'sum'),
        dias_secos_total=('dia_seco', 'sum'),
        oni_medio=('oni', 'mean'),
        soi_medio=('soi', 'mean')
    ).reset_index()
    
    # 4. Merge Base Soja (alvo) + Clima Anual
    print("Cruzando Soja e Clima...")
    df_final = pd.merge(df_soja, df_clima_anual, on=['CD_MICRO', 'ano'], how='left')
    
    # 5. Merge Base + Solo Estático (SoilGrids)
    print("Cruzando com Solo (estático)...")
    df_final = pd.merge(df_final, df_solo, on='CD_MICRO', how='left')
    
    print(f"Base final consolidada com {df_final.shape[0]} linhas e {df_final.shape[1]} colunas.")
    return df_final
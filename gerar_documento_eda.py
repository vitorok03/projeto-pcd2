import json
import os
import base64
from pathlib import Path

pasta_eda = Path("notebooks/eda")
arquivo_saida = "documento_eda_completo.html"

notebooks = {
    "eda_clima_horario_diario.ipynb": "1. ANÁLISE EXPLORATÓRIA: CLIMA (INMET)",
    "eda_soja.ipynb": "2. ANÁLISE EXPLORATÓRIA: SOJA (SIDRA/IBGE)",
    "eda_solo.ipynb": "3. ANÁLISE EXPLORATÓRIA: SOLO (SoilGrids)",
    "eda_correlacao_anomalias.ipynb": "4. ANÁLISE EXPLORATÓRIA: ANOMALIAS DO PACÍFICO (ONI/SOI) E INTEGRAÇÃO"
}

# Início do HTML com um CSS básico para ficar bonito
html_final = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Relatório EDA - Soja e Clima</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; margin: 40px; color: #333; }
        h1 { color: #2c3e50; border-bottom: 2px solid #2c3e50; padding-bottom: 10px; }
        h2 { color: #34495e; margin-top: 40px; border-bottom: 1px solid #ccc; padding-bottom: 5px; }
        pre { background-color: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; font-size: 14px; }
        code { font-family: Consolas, "Courier New", monospace; }
        .text-cell { background-color: #e8f4f8; padding: 15px; border-left: 5px solid #3498db; margin: 15px 0; border-radius: 4px; }
        .image-container { text-align: center; margin: 20px 0; }
        .image-container img { max-width: 100%; height: auto; border: 1px solid #ddd; box-shadow: 2px 2px 8px rgba(0,0,0,0.1); }
    </style>
</head>
<body>
<h1>Relatório Completo de Análise Exploratória de Dados (EDA) - Projeto Soja & Clima</h1>
<p>Este documento contém os códigos, análises descritivas e gráficos gerados para a base de dados de produtividade de soja, clima, solo e anomalias do Pacífico.</p>
"""

for arquivo, titulo in notebooks.items():
    caminho = pasta_eda / arquivo
    if not caminho.exists():
        print(f"Pulando {arquivo} (não encontrado).")
        continue
        
    html_final += f"<h2>{titulo}</h2>\n"
    
    with open(caminho, 'r', encoding='utf-8') as f:
        nb = json.load(f)
        
    for celula in nb['cells']:
        tipo = celula['cell_type']
        conteudo = "".join(celula['source'])
        
        if not conteudo.strip():
            continue
            
        # 1. Textos (Markdown)
        if tipo == 'markdown':
            # Substitui quebras de linha por <br> para formatar bem no HTML
            texto_formatado = conteudo.replace('\n', '<br>')
            html_final += f'<div class="text-cell"><strong>[Análise]:</strong><br>{texto_formatado}</div>\n'
            
        # 2. Códigos e Gráficos
        elif tipo == 'code':
            # Adiciona o código
            html_final += f"<pre><code>{conteudo}</code></pre>\n"
            
            # Adiciona as imagens geradas por esse código
            if 'outputs' in celula:
                for output in celula['outputs']:
                    if 'data' in output and 'image/png' in output['data']:
                        # Pega a imagem em base64
                        img_base64 = output['data']['image/png']
                        html_final += f'<div class="image-container"><img src="data:image/png;base64,{img_base64}"></div>\n'

html_final += "</body>\n</html>"

with open(arquivo_saida, 'w', encoding='utf-8') as f:
    f.write(html_final)

print(f"✅ Documento HTML com gráficos gerado com sucesso: {arquivo_saida}")
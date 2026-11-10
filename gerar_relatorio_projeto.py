import json
import os
import base64
from pathlib import Path

# Pastas onde estão seus notebooks
pastas_alvo = [Path("notebooks/eda"), Path("notebooks/pipeline"), Path(".")]
arquivo_saida = "relatorio_completo_projeto.html"

# Mapeamento dos arquivos (ajuste os nomes se necessário)
notebooks = {
    "eda_clima_horario_diario.ipynb": "1. EDA Clima (INMET)",
    "eda_soja.ipynb": "2. EDA Soja (SIDRA)",
    "eda_solo.ipynb": "3. EDA Solo (SoilGrids)",
    "eda_correlacao_anomalias.ipynb": "4. EDA Correlação e Anomalias (Pacífico)",
    "06_feature_engineering_e_insights.ipynb": "5. Feature Engineering e Clusters" # Se você criou este notebook
}

# Template HTML com CSS
html_final = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Relatório EDA - Soja e Clima</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; margin: 40px; color: #333; max-width: 1200px; }
        h1 { color: #2c3e50; border-bottom: 2px solid #2c3e50; padding-bottom: 10px; }
        h2 { color: #34495e; margin-top: 40px; border-bottom: 1px solid #ccc; padding-bottom: 5px; }
        pre { background-color: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; font-size: 13px; border-left: 4px solid #7f8c8d; }
        code { font-family: Consolas, "Courier New", monospace; }
        .text-cell { background-color: #e8f4f8; padding: 15px; border-left: 5px solid #3498db; margin: 15px 0; border-radius: 4px; }
        .image-container { text-align: center; margin: 30px 0; }
        .image-container img { max-width: 100%; height: auto; border: 1px solid #ddd; box-shadow: 2px 2px 8px rgba(0,0,0,0.1); }
    </style>
</head>
<body>
<h1>Relatório Completo de Análise Exploratória (EDA) e Feature Engineering</h1>
<p>Este documento contém os códigos, análises descritivas e gráficos gerados para o projeto.</p>
"""

for arquivo, titulo in notebooks.items():
    caminho = None
    for pasta in pastas_alvo:
        if (pasta / arquivo).exists():
            caminho = pasta / arquivo
            break
            
    if not caminho:
        print(f"Pulando {arquivo} (não encontrado).")
        continue
        
    print(f"Processando {arquivo}...")
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
            texto_formatado = conteudo.replace('\n', '<br>')
            html_final += f'<div class="text-cell"><strong>[Análise]:</strong><br>{texto_formatado}</div>\n'
            
        # 2. Códigos e Gráficos
        elif tipo == 'code':
            # Escapa caracteres HTML do código para não quebrar a página
            codigo_escapado = conteudo.replace('<', '&lt;').replace('>', '&gt;')
            html_final += f"<pre><code>{codigo_escapado}</code></pre>\n"
            
            # Adiciona as imagens geradas por esse código
            if 'outputs' in celula:
                for output in celula['outputs']:
                    if 'data' in output and 'image/png' in output['data']:
                        img_base64 = output['data']['image/png']
                        html_final += f'<div class="image-container"><img src="data:image/png;base64,{img_base64}"></div>\n'

html_final += "</body>\n</html>"

with open(arquivo_saida, 'w', encoding='utf-8') as f:
    f.write(html_final)

print(f"\n✅ Relatório HTML com imagens gerado com sucesso: {arquivo_saida}")
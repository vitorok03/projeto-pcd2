---
tipo: projeto
fonte: readme
tags: [projeto, limitacoes]
---
# Limitações conhecidas

Do README:
- A cobertura de estações do INMET cresce muito ao longo do tempo; safras antigas perdem mais linhas por baixa [[Completude]] ([[Q04 Recorte temporal inicial]]).
- Algumas microrregiões não têm estação dentro; recebem clima de uma estação substituta (coluna `origem`), com limite de 150 km ([[D06 Distância máxima de 150 km]]).

Da análise do projeto:
- Agregar por microrregião ainda suaviza a variação climática dentro dela ([[D01 Microrregião em vez de UF]]).
- Microrregiões do Norte têm malha rala; algumas produtoras ficam sem clima ([[Q01 Microrregiões produtoras fora da base final]]).
- Extremos (temp. máx./mín.) podem subestimar o valor real mesmo com [[Completude]] alta ([[D04 Limiar de completude de 80 por cento]]).
- Rendimento sobe com a tecnologia, independente do clima ([[D15 Tendência tecnológica e detrending]]).
- Pouca amostra por microrregião favorece modelos simples ([[D08 Validação temporal e baselines]]).

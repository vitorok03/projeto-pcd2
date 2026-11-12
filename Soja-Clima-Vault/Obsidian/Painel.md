---
tipo: painel
tags: [painel]
---
# Painel

Requer o plugin **Dataview**. Se não quiser instalá-lo, use as listas estáticas no fim.

## Questões abertas
```dataview
TABLE id, status FROM "08 - Questões em aberto"
WHERE status != "resolvida"
SORT id ASC
```

## Notas a confirmar contra o código
```dataview
LIST FROM ""
WHERE fonte = "a-confirmar"
SORT file.name ASC
```

## Decisões
```dataview
TABLE status, fonte FROM "06 - Decisões"
SORT id ASC
```

## Problemas
```dataview
TABLE status FROM "07 - Problemas e soluções"
SORT id ASC
```

## Lista estática (sem Dataview)
- Em aberto: [[Q01 Microrregiões produtoras fora da base final]], [[Q02 Arquivos de 2005 com formato diferente]], [[Q05 Defasagem dos índices ONI e SOI]], [[Q06 Método de detrending]], [[Q07 Modelos e resultados]], [[Q08 Cobertura de testes]]
- Resolvidas: [[Q03 Ponderação por completude foi mantida]], [[Q04 Recorte temporal inicial]]
- A confirmar no código: [[Módulo clima]], [[Testes]], [[EDA Solo]], [[EDA Correlação e Anomalias]], [[Feature Engineering e Clusters]], [[Q07 Modelos e resultados]], [[Q08 Cobertura de testes]]
- Riscos do código: [[Pontos de atenção do código]]

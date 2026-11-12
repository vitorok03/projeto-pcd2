---
tipo: decisao
id: D07
status: substituida
fonte: codigo
criado: 2026-11-10
tags: [decisao]
---
# D07: Fases fenológicas


## Histórico
- Desenho original: quatro fases (plantio 0–39 dias, vegetativo 40–89, floração/enchimento 90–129, maturação 130–240).
- Decisão intermediária: começar só com a **safra completa** (`usar_fases=False`) para validar o pipeline e ter um baseline.

## Estado atual (confirmado no `main.ipynb`)
Os dois: `agregar_diario_para_estacao_safra(usar_fases=True)` + `agregar_espacial_para_microrregiao` geram as fases, e `merge.agregar_clima_micro_safra` gera a **safra inteira**. As duas versões entram na base final. Esta decisão foi substituída.

## Por que importa
O mesmo déficit hídrico pesa muito mais na floração/enchimento do que na maturação; a safra inteira dilui esse sinal.

## A confirmar
Limites de dias de cada fase no código atual (os acima são os da versão das conversas).

Relacionado: [[Módulo agregacao]] · [[Pergunta de pesquisa]]

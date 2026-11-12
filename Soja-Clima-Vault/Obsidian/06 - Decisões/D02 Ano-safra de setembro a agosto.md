---
tipo: decisao
id: D02
status: ativa
fonte: conversa
criado: 2026-11-10
tags: [decisao]
---
# D02: Ano-safra de setembro a agosto


## Contexto
A soja é plantada entre setembro e dezembro e colhida entre janeiro e maio. Agrupar por ano civil misturaria duas safras.

## Decisão
`safra = ano + 1` se o mês for ≥ 9; janela de 241 dias a partir de 1º de setembro. A safra recebe o ano em que termina, para casar com o "ano" do SIDRA (o `merge.py` documenta que a safra é rotulada pelo ano da colheita, "o mesmo `ano` do PAM/SIDRA").

## Consequências
Arquivos de um ano civil alimentam duas safras. Anos com cobertura parcial geram baixa [[Completude]].

Relacionado: [[Ano-safra]] · [[Módulo agregacao]] · [[D07 Fases fenológicas]]

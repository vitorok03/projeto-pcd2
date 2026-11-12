---
tipo: questao
id: Q01
status: aberta
fonte: conversa
tags: [questao]
---
# Q01: Microrregiões produtoras fora da base final


## Pergunta
Por que 5 microrregiões produtoras ficaram fora da base final?

## Contexto
| code_micro | Nome | UF |
|---|---|---|
| 11005 | Alvorada d'Oeste | RO |
| 14003 | Caracaraí | RR |
| 14004 | Sudeste de Roraima | RR |
| 13009 | Itacoatiara | AM |
| 13004 | Juruá | AM |

Duas ficaram sem clima algum (nenhuma estação a menos de 150 km). As outras três **tinham estação atribuída** (A121 → 13009, A109 → 13004, S113 → 14004) com [[Completude]] boa na maioria dos anos, mas nenhum ano chegou à base final.

## Hipóteses
- Tipo do `code_micro` diferente entre os lados do merge (float × texto). O código agora padroniza com `_padronizar_cd_micro` ([[P12 Código da microrregião como float ou texto]]), então vale **reexecutar** antes de investigar mais
- Erro no mapeamento estação → `code_micro` antes da agregação
- Os novos filtros ([[D16 Filtros da base de modelagem]]: área ≥ 100 ha, ano ≥ 2009) podem ter removido algumas de propósito

## Como testar
Reexecutar o `main`; comparar `dtype` de `code_micro` em clima e produção; checar se os cinco códigos existem em `clima_micro_safra` e em `df_soja_micro`; descontar o que os filtros removeram.

Relacionado: [[P07 Denominador de 558 microrregiões]] · [[D06 Distância máxima de 150 km]] · [[main — base final de modelagem]]

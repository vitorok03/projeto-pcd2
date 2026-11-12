---
tipo: problema
id: P08
status: resolvido
fonte: conversa
tags: [problema]
---
# P08: Coordenadas divergentes e índice duplicado


**Sintoma:** 548 de 614 estações com coordenadas diferentes entre arquivos; `ValueError: cannot reindex on an axis with duplicate labels` (estação `A302` duplicada).

**Causa:** a mesma estação com lat/lon diferindo na 4ª/5ª casa decimal entre anos (ordem de metros: benigno). Tabela de estações com `codigo_estacao` repetido quebrava `.loc` por índice.

**Correção:** deduplicar por código usando a **mediana** das coordenadas; trocar `.loc` por `merge` + `fillna`.

Relacionado: [[Módulo geo]]

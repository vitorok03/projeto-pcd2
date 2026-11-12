---
tipo: problema
id: P09
status: resolvido
fonte: conversa
tags: [problema]
---
# P09: Avisos e mudanças do pandas


- Colunas de texto reportadas como dtype `str` (não `object`) em versões novas: a checagem `dtype == object` deixava de converter números com vírgula. Usar `pd.api.types.is_numeric_dtype`.
- `DeprecationWarning` em `groupby().apply`: passar `include_groups=False`.
- `SettingWithCopyWarning`: usar `.copy()` onde a tabela é criada.

Relacionado: [[Módulo sidra]] · [[Módulo agregacao]]

---
tipo: problema
id: P05
status: resolvido
fonte: conversa
tags: [problema]
---
# P05: glob duplica arquivos no Windows


**Sintoma:** o diagnóstico contava ~18 mil arquivos; no Colab eram ~9 mil.

**Causa:** em sistemas de arquivos que não diferenciam maiúscula de minúscula (Windows, macOS), `*.CSV` e `*.csv` casam os mesmos arquivos. Concatenar as duas listas dobra o total. No Linux (Colab) um dos padrões não casava nada.

**Correção:** `sorted(set(glob(...) + glob(...)))`.

**Prevenção:** deduplicar sempre; ou usar um único padrão case-insensitive.

Relacionado: [[Etapa 01 — Processar clima]]

---
tipo: problema
id: P10
status: resolvido
fonte: conversa
tags: [problema]
---
# P10: Google Drive lento no Colab


**Sintoma:** `No such file or directory` ao ler arquivos que o `glob` listava; leitura lenta de milhares de arquivos pequenos.

**Causa:** o Drive montado (FUSE) lista arquivos antes de sincronizar o conteúdo e tem latência por arquivo.

**Correção histórica:** copiar para o disco local da VM em paralelo (threads, retry por arquivo). **Resolvido de vez** ao sair do Colab: [[D10 Pacote src e notebooks]].

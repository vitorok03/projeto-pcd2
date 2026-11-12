---
tipo: problema
id: P01
status: resolvido
fonte: conversa
tags: [problema]
---
# P01: Formato do INMET muda entre anos


**Sintoma:** erros de coluna não encontrada ou `KeyError: 'ESTACAO'` ao ler anos diferentes.

**Causa:**

| Período | Mudança |
|---|---|
| até 2018 | colunas `DATA (YYYY-MM-DD)` e `HORA (UTC)`, data com `-` |
| 2019 | colunas `Data` e `Hora UTC` (`0000 UTC`), data com `/`; metadados corrompidos (`REGI?O`, `ESTAC?O`, `DATA DE FUNDAC?O`) |
| 2020+ | `RADIACAO GLOBAL (Kj/m²)` com "j" minúsculo; mais casas decimais em lat/lon |

**Correção:** detectar data/hora por prefixo; comparar nomes de coluna em maiúsculo; `normalizar_chave_meta`; `ValueError` explícito listando colunas essenciais ausentes.

**Prevenção:** validar o parser em um arquivo de cada era antes de rodar o lote. Pendência: [[Q02 Arquivos de 2005 com formato diferente]].

Relacionado: [[Módulo inmet]] · [[INMET — estações automáticas]]

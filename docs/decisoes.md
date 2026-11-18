# Registro de decisões metodológicas

Este arquivo registra **por que escolhemos x e não y** em cada decisão de método do projeto.
Cada decisão traz o contexto, as opções consideradas, a evidência que sustentou a escolha e as
limitações conhecidas. Quando uma decisão for revista, a entrada antiga **não é apagada**: muda
o status para "Substituída por D-xx".

| ID | Decisão | Status | Data |
|---|---|---|---|
| [D-01](#d-01--divisão-regional-para-a-análise-do-enso) | Divisão regional para a análise do ENSO | Adotada (reavaliada com defasagens) | 2026-11-17 |
| [D-02](#d-02--critério-para-identificar-defasagens-entre-o-enso-e-a-chuva) | Critério para identificar defasagens entre o ENSO e a chuva | Adotada | 2026-11-18 |
| [D-03](#d-03--defasagens-encontradas-e-nível-de-evidência-por-região) | Defasagens encontradas e nível de evidência por região | Adotada; níveis revisados pelo D-04 | 2026-11-18 |
| [D-04](#d-04--teste-de-significância-por-séries-substitutas) | Teste de significância por séries substitutas | Adotada (revisão dos níveis aprovada) | 2026-11-18 |
| [D-05](#d-05--relação-enso--chuva-por-subperíodo-da-safra) | Relação ENSO × chuva por subperíodo da safra | Adotada (resultado de análise) | 2026-11-18 |
| [D-06](#d-06--chuva-da-safra-por-fase-do-enso) | Chuva da safra por fase do ENSO | Adotada (resultado de análise) | 2026-11-18 |
| [D-07](#d-07--sensibilidade-às-escolhas-de-método) | Sensibilidade às escolhas de método | Adotada (resultado de análise) | 2026-11-18 |
| [D-08](#d-08--outras-variáveis-climáticas-e-o-enso) | Outras variáveis climáticas e o ENSO | Adotada (resultado de análise) | 2026-11-18 |
| [D-09](#d-09--série-longa-de-rendimento-pam-19742025-dados-e-método) | Série longa de rendimento (PAM 1974–2025): dados e método | Adotada | 2026-11-18 |
| [D-10](#d-10--enso--rendimento-da-soja-resultados) | ENSO × rendimento da soja: resultados | Adotada (resultado de análise) | 2026-11-18 |
| [D-11](#d-11--cadeia-enso--chuva--rendimento-desenho-da-análise) | Cadeia ENSO → chuva → rendimento: desenho da análise | Adotada | 2026-11-18 |
| [D-12](#d-12--cadeia-enso--chuva--rendimento-resultados) | Cadeia ENSO → chuva → rendimento: resultados | Adotada (resultado de análise) | 2026-11-18 |

---

## D-01 · Divisão regional para a análise do ENSO

- **Status:** adotada. Era provisória e foi confirmada na reavaliação com defasagens (ver "Reavaliação com defasagens", no fim desta entrada).
- **Notebook:** `notebooks/eda/eda_enso_defasagens.ipynb` (seções 4 a 8 e 14)

### Contexto
O ENSO afeta o Brasil com sinais **opostos**: o El Niño tende a aumentar a chuva no Sul e a
reduzi-la no Norte e no Nordeste. Uma análise nacional cancela esses efeitos, então a divisão
regional precisa ser escolhida **antes** da varredura de defasagens. Se não for assim, a defasagem
seria escolhida sobre um sinal que se anula.

A resposta usada foi a **anomalia mensal de chuva**, e não o rendimento:
- **é o mecanismo físico**: o ENSO muda a chuva, e a chuva muda o rendimento;
- **tem mais amostra**: 173 meses de safra (2005–2026), com mediana de 133 meses válidos por
  microrregião, contra 17 a 26 safras de rendimento;
- **independe do `desvio_clima`**, que ainda é nacional.

### Opções consideradas
| Divisão | Nº de regiões com dados | Observação |
|---|---|---|
| Macrorregião (IBGE) | 5 | |
| UF | 23 | |
| UF, com UFs pequenas agrupadas na macrorregião | 21 | AP, CE, DF, PB, RJ e RR tinham menos de 3 microrregiões com dados |
| Bioma (IBGE 2019) | 6 | microrregião atribuída ao bioma de maior área |
| Bioma, com o Pantanal agrupado ao Cerrado | 5 | o Pantanal tinha só 2 microrregiões com dados |
| Região geográfica intermediária (IBGE 2017) | 94 | mediana de 2 microrregiões por região |
| Macrorregião + MATOPIBA | 6 | MATOPIBA **aproximado**: MA/TO/PI/BA com predomínio de Cerrado (33 microrregiões; a delimitação oficial tem 31) |
| Regiões edafoclimáticas da soja (Embrapa) | — | **não avaliada**: o mapa não estava disponível; o notebook lê `data/raw/regioes/rec_soja.csv` se existir |

### Decisões de método da análise
| Escolha | Alternativa descartada | Motivo |
|---|---|---|
| Anomalia padronizada **por mês do calendário** | chuva em mm | remove a sazonalidade; "janeiro chuvoso" e "agosto chuvoso" não são comparáveis em mm |
| Só os meses da safra (set–abr) | ano inteiro | é a janela do pipeline; os meses secos têm desvio próximo de zero, o que torna a anomalia instável |
| Mês da estação válido com ≥ 80% dos dias | qualquer dia disponível | uma soma com lacunas subestima a chuva (mesmo critério do pipeline) |
| Média entre as estações da microrregião | soma | estações são amostras do mesmo campo de chuva (mesmo critério do pipeline) |
| Só estações **dentro** da microrregião | incluir estações substitutas | uma substituta repete a mesma estação em várias microrregiões e infla artificialmente a semelhança entre vizinhas |
| Correlação de **Spearman** | Pearson | a chuva é assimétrica; a correlação de postos é robusta a meses extremos |
| p-valor com **amostra efetiva** (Bretherton et al., 1999) | n de meses | o ONI é uma média móvel de 3 meses, muito autocorrelacionada; meses vizinhos não são independentes |
| Correção **FDR (Benjamini–Hochberg)** | p-valor bruto | são centenas de testes (um por microrregião) |
| Escolha da divisão pela **validação fora da amostra** | métricas dentro da amostra | ver "Evidência" abaixo |

### Evidência

**1. As métricas dentro da amostra apontavam para a escolha errada.** O R² ajustado da
homogeneidade (quanto a divisão explica da variação da resposta entre microrregiões, nos mesmos
anos usados para calculá-la) colocava UF (0,54) e Região intermediária (0,51) no topo, e Bioma
(0,27) por último. Essas métricas favorecem divisões com muitas regiões pequenas, que se ajustam
ao ruído.

**2. Validação fora da amostra (critério adotado).** O ρ de cada microrregião foi estimado só
com as safras pares e, separadamente, só com as ímpares. A média do ρ das *outras* microrregiões
da região, estimada num conjunto, previu o ρ da microrregião no outro conjunto, nos dois sentidos.

| Divisão | R² fora, defasagem 0 | R² fora, defasagem 3 | Erro pond. pela produção (def. 0 / 3) | Repetição do ρ regional (def. 0 / 3) |
|---|---|---|---|---|
| Sem divisão (média nacional), referência | −0,002 | −0,001 | 0,203 / 0,199 | — |
| **Bioma (Pantanal → Cerrado)** | **−0,094** | **−0,060** | **0,210 / 0,200** | **0,45 / 0,59** |
| Bioma (IBGE) | −0,095 | −0,070 | 0,210 / 0,201 | 0,45 / 0,59 |
| Macrorregião | −0,139 | −0,114 | 0,231 / 0,226 | 0,22 / 0,42 |
| UF | −0,090 | −0,193 | 0,226 / 0,227 | 0,44 / 0,36 |
| UF (pequenas → macrorregião) | −0,092 | −0,192 | 0,226 / 0,227 | 0,37 / 0,27 |
| Macrorregião + MATOPIBA | −0,157 | −0,134 | 0,232 / 0,226 | 0,12 / 0,30 |
| Região intermediária | −0,340 | −0,374 | 0,248 / 0,239 | 0,32 / 0,25 |

**3. No nível da microrregião, a resposta ao ENSO é dominada por ruído.** O ρ de uma
microrregião se repete pouco entre metades das safras: a correlação entre as metades é 0,17 na
defasagem 0 e 0,15 na defasagem 3, ou cerca de 0,28 estimado para a série inteira pela fórmula de
Spearman-Brown. Por isso **nenhuma divisão supera a média nacional fora da amostra**. Agregar em
regiões melhora a repetibilidade do sinal (de 0,22 a 0,59), pelo mesmo princípio da média entre
estações.

**4. Resposta regional com a divisão escolhida** (ONI × anomalia de chuva, defasagem 0):

| Bioma | ρ | Significativo (FDR 5%) | Microrregiões | Produção média (Mt) |
|---|---|---|---|---|
| Amazônia | −0,19 | não | 37 | 12,5 |
| Caatinga | −0,15 | não | 11 | 0,04 |
| Cerrado (+ Pantanal) | −0,01 | não | 80 | 54,9 |
| Mata Atlântica | +0,16 | não | 84 | 18,4 |
| Pampa | +0,28 | **sim** | 16 | 7,7 |

O mapa do SOI é o espelho do ONI (correlação de −0,92 entre os dois mapas), o que confirma a
consistência dos índices.

### Decisão
**Divisão provisória: Bioma (IBGE), com o Pantanal agrupado ao Cerrado (5 regiões). A UF entra
como análise de sensibilidade.**

### Por quê
- **Bioma (Pantanal → Cerrado):**
  - tem o melhor R² fora da amostra médio entre as divisões avaliadas;
  - tem o menor erro ponderado pela produção nas duas defasagens;
  - tem a maior repetibilidade do sinal regional;
  - tem motivação física, porque os biomas refletem regimes de clima;
  - com 5 regiões, a varredura de defasagens fica em 5 × 13 defasagens × 3 janelas, um número de testes controlável;
  - agrupar o Pantanal (2 microrregiões) ao Cerrado, vizinho e de clima semelhante, evita uma região frágil sem perder desempenho.
- **UF (sensibilidade):** empata com o Bioma sem defasagem, mas piora com 3 meses e tem
  regiões com 1 ou 2 microrregiões. Fica como checagem e para comunicação ("por estado" é intuitivo).
- **Descartadas:**
  - **Região intermediária:** pior fora da amostra, com regiões pequenas demais (34% das microrregiões em regiões com menos de 3 membros);
  - **Macrorregião + MATOPIBA:** separar o MATOPIBA não melhora nenhuma métrica, e a delimitação é aproximada;
  - **Macrorregião:** fica abaixo do Bioma em todas as métricas fora da amostra.

### Consequências e limitações
- **A margem é pequena.** Todas as divisões ficam abaixo de zero fora da amostra, e as diferenças
  entre Bioma, UF e Macrorregião são pequenas. O que os dados sustentam com segurança é a
  **gangorra Sul (+) × Norte (−) em escala grande**, não uma divisão fina.
- **O sinal sem defasagem é fraco:** só 10% das microrregiões têm correlação significativa
  com o ONI. O **Cerrado, que concentra a maior parte da soja, não responde sem defasagem**
  (ρ = −0,01). Isso pode mudar com a defasagem certa, então a divisão deve ser **reavaliada depois
  da varredura de defasagens**.
- **A escolha usou todas as safras de 2005 a 2026.** Para não reaproveitar os mesmos anos, as **safras
  de 2021 a 2025 ficam reservadas** como teste final a partir da varredura de defasagens.
- **Outras limitações:**
  - cada metade da validação tem só cerca de 10 safras;
  - a amostra efetiva é uma aproximação (autocorrelação de defasagem 1);
  - o MATOPIBA é aproximado;
  - as regiões da Embrapa não foram avaliadas;
  - 228 das 310 microrregiões com soja têm estação dentro do polígono (as demais dependem de estações substitutas, excluídas desta análise).

### Reavaliação com defasagens (2026-11-18)
A validação fora da amostra foi repetida só com as safras de exploração (até 2020), nas defasagens
de 0, 3, 6 e 9 meses (janela de 1 mês):

| Divisão | R² fora: def. 0 | def. 3 | def. 6 | def. 9 | Média | Posição média |
|---|---|---|---|---|---|---|
| Sem divisão (referência) | −0,007 | −0,005 | −0,055 | −0,004 | −0,018 | — |
| **Bioma (Pantanal → Cerrado)** | −0,164 | −0,118 | −0,357 | −0,006 | **−0,161** | **2,25** |
| Bioma (IBGE) | −0,160 | −0,122 | −0,381 | −0,032 | −0,174 | 3,00 |
| Macrorregião | −0,203 | −0,149 | −0,363 | +0,018 | −0,174 | 2,75 |
| Macrorregião + MATOPIBA | −0,203 | −0,159 | −0,388 | −0,004 | −0,188 | 4,00 |
| UF (pequenas → macrorregião) | −0,144 | −0,170 | −0,661 | −0,237 | −0,303 | 4,25 |
| UF | −0,157 | −0,204 | −0,694 | −0,235 | −0,322 | 4,75 |
| Região intermediária | −0,455 | −0,446 | −0,998 | −0,590 | −0,622 | 7,00 |

**Resultado:** a escolha se mantém. O Bioma (Pantanal → Cerrado) tem a melhor média e a melhor
posição média com qualquer defasagem. O R² fora da amostra continua negativo em todas as divisões:
a resposta de cada microrregião isolada segue dominada por ruído, e a divisão serve para **agregar**
o sinal, não para prever microrregiões individuais.

---

## D-02 · Critério para identificar defasagens entre o ENSO e a chuva

- **Status:** adotada.
- **Notebook:** `notebooks/eda/eda_enso_defasagens.ipynb` (Parte 2, seções 9 a 12)

### Contexto
O ENSO pode afetar a chuva com atraso. Para cada região (D-01), foram comparadas a anomalia mensal
de chuva da safra (set–abr) e o **índice ENSO defasado**: a média do índice nos *w* meses que terminam
*L* meses antes do mês da chuva, com L de 0 a 12 e w de 1, 3 ou 6. São **195 combinações por índice**
na divisão por bioma (5 × 13 × 3) e 819 na divisão por UF.

Esta é uma **análise de dados**, não um modelo de previsão: a pergunta é com quantos meses de atraso
a chuva de cada região mais se relaciona com o ENSO, e se o padrão se repete em outro período.

**Os períodos foram separados antes da análise:**
- **exploração:** safras de 2005 a 2020 (124 meses), onde os padrões são procurados;
- **verificação de robustez:** safras de 2021 a 2025 (40 meses), usadas **uma única vez**, depois de
  fixados os critérios.

### O problema encontrado na exploração
O critério original (o ONI com correção FDR) **não aprovou nenhuma combinação** nos biomas: o menor
p corrigido foi 0,08. Os mapas de calor, porém, mostram padrões contínuos, coerentes com a física e
espelhados no SOI. A correção ficou muito conservadora porque as 195 combinações são fortemente
redundantes (defasagens vizinhas e janelas sobrepostas medem quase o mesmo), e o ONI, já suavizado
em 3 meses, tem amostra efetiva pequena.

### Opções consideradas (todas avaliadas só com as safras até 2020)
| Opção | Critério | Biomas aprovados | UFs aprovadas |
|---|---|---|---|
| 3 · ONI + FDR (original) | combinação do ONI significativa após o FDR | 0 de 5 | 1 de 21 (MT) |
| 1 · índice combinado + FDR | o mesmo, com o índice z(ONI) − z(SOI) | 1 de 5 (Amazônia) | 1 de 21 (MT) |
| 2 · ONI + consistência | maior \|ρ\| suavizado + platô + SOI concordante + estabilidade | 4 de 5 | 10 de 21 |

O índice combinado quase não ajudou: o ONI e o SOI são muito correlacionados (r = −0,72 mês a mês), e
juntá-los reduz pouco o ruído.

### Decisão
**Procedimento em duas etapas, com níveis de evidência:**
1. **Exploração (safras até 2020):** a opção 2 aponta os **padrões candidatos**. Para cada região, a
   defasagem e a janela com o maior |ρ| do ONI, suavizado entre as defasagens vizinhas, passam a
   candidatas se cumprirem os três critérios:
   - **platô:** as defasagens vizinhas (L − 1 e L + 1) têm o mesmo sinal e |ρ| médio de pelo menos 2/3 do pico;
   - **SOI concordante:** a defasagem escolhida pelo SOI está a até 2 meses da do ONI, com sinal oposto;
   - **estabilidade:** o ρ tem o mesmo sinal nas safras pares e nas ímpares.
2. **Verificação (safras de 2021 a 2025), uma única vez**, com a mesma defasagem e janela. **"Se
   repete"** = mesmo sinal da exploração e |ρ| ≥ 0,10.
3. **Níveis de evidência:**

| Nível | Critério |
|---|---|
| forte | candidato que também passa no FDR (opção 1 ou 3) e se repete |
| moderada | candidato que se repete |
| não confirmada | candidato que não se repete |
| sem padrão consistente | não é candidato |

### Por quê
- **Separar exploração e verificação** é uma forma reconhecida de controlar achados ao acaso. Ela
  substitui o FDR quando este é rígido demais por causa da redundância entre os testes.
- **Os níveis de evidência** permitem relatar o padrão completo sem esconder o grau de certeza: só o
  que passa no FDR é chamado de "forte".
- **A opção 3 sozinha** contradiria a análise por UF: o MT passa no FDR com 5 meses de defasagem, mas
  o Cerrado, que o contém, ficaria "sem defasagem".
- **A opção 1 sozinha** mantém o rigor, mas descarta padrões consistentes, como o do Cerrado, que
  depois se confirmaram no período independente.

### Transparência sobre a mudança de critério
A mudança da opção 3 para o procedimento em duas etapas foi feita **depois** de ver os resultados da
exploração, mas **antes** de olhar as safras de 2021 a 2025. Os limites da opção 2 (2/3 do pico e
tolerância de 2 meses) também foram definidos nesse momento. O critério da verificação (mesmo sinal e
|ρ| ≥ 0,10) foi fixado no notebook antes da execução que usou essas safras.

### Limitações
- A verificação tem só 5 safras (cerca de 40 meses). Ela mostra se o sinal **se mantém**, e quase todos
  os intervalos de confiança de 95% cruzam o zero.
- A concordância com o SOI não é uma evidência independente, porque os dois índices medem o mesmo fenômeno.

---

## D-03 · Defasagens encontradas e nível de evidência por região

- **Status:** adotada.
- **Notebook:** `notebooks/eda/eda_enso_defasagens.ipynb` (seções 12, 13, 15 e 16)

> **Atualização (D-04, aprovada):** o critério de evidência "forte" passou a ser o teste por séries substitutas, e não o FDR. Com isso, **o Cerrado e o GO passam a forte, e a Amazônia a moderada**. As tabelas abaixo mostram os níveis originais; os níveis vigentes estão no D-04.

### Resultados (ONI)
**Por bioma (divisão principal):**

| Bioma | Defasagem | Janela | ρ exploração | ρ 2021–2025 (IC 95%) | ρ 2021–2025 sem defasagem | Nível | Soja (Mt/ano) |
|---|---|---|---|---|---|---|---|
| Amazônia | 2 meses | 6 | −0,34 | −0,38 [−0,58; +0,17] | −0,23 | **forte** | 12,5 |
| **Cerrado** | **7 meses** | 3 | −0,29 | −0,28 [−0,57; +0,25] | −0,06 | moderada | **54,9** |
| Pampa | 0 meses | 1 | +0,22 | +0,41 [−0,14; +0,65] | +0,41 | moderada | 7,7 |
| Caatinga | 3 meses | 6 | −0,22 | +0,06 [−0,30; +0,53] | −0,04 | não confirmada | 0,04 |
| Mata Atlântica | — | — | — | — | — | sem padrão consistente (instável entre metades) | 18,4 |

**Por UF (sensibilidade), principais produtoras:**

| UF | Bioma predominante (pela produção) | Defasagem | ρ exploração | ρ 2021–2025 | Nível | Soja (Mt/ano) |
|---|---|---|---|---|---|---|
| MT | Cerrado | 5 meses (janela 6) | −0,41 | −0,16 | **forte** | 29,4 |
| GO | Cerrado | 8 meses | −0,28 | −0,13 | moderada | 10,9 |
| MG | Cerrado | 8 meses (janela 3) | −0,17 | −0,14 | moderada | 5,1 |
| PA | Amazônia | 0 meses (janela 3) | −0,39 | −0,56 | moderada | 1,7 |
| MS | Cerrado | 9 meses | −0,19 | −0,04 | não confirmada | 8,5 |
| BA | Cerrado | 3 meses | −0,19 | +0,08 | não confirmada | 5,1 |
| RS, PR, SC | Pampa / Mata Atlântica | — | — | — | sem padrão consistente | 23,5 |

### Conclusões
1. **Gangorra Norte–Sul:** em anos de El Niño, a chuva da safra tende a ser menor no Norte e no
   Centro-Oeste e maior no Sul (Pampa), como descreve a literatura sobre o ENSO no Brasil.
2. **A resposta é imediata no Sul e na Amazônia e atrasada no Cerrado.** No Cerrado e nas UFs dele
   (MT, GO, MG), a relação mais forte aparece com 5 a 8 meses de defasagem e quase não existe sem
   defasagem. É o resultado mais relevante, porque o Cerrado concentra a maior parte da soja da base.
   Na verificação, o ρ do Cerrado com 7 meses se repetiu (−0,28), contra −0,06 sem defasagem.
3. **As correlações são moderadas** (|ρ| entre 0,15 e 0,4): o ENSO explica parte da variação da chuva,
   não a maior parte.

### Como cada caso segue daqui em diante
| Nível | Uso nas próximas etapas |
|---|---|
| forte / moderada | entra como variável de ENSO defasado do bioma (defasagem e janela acima) quando o pipeline for estendido; relatado como resultado |
| não confirmada | fica com a janela padrão da safra (set–abr, sem defasagem); relatado como "padrão não confirmado" |
| sem padrão consistente | fica com a janela padrão; relatado como tal |

### Cautelas e limitações
- No MT, a relação se repetiu mais fraca (−0,41 → −0,16), e a correlação sem defasagem mudou de sinal
  em 2021–2025 (+0,32).
- No Sul, o sinal sem defasagem é claro no Pampa, mas instável nas UFs (RS, PR e SC).
- A análise usa a chuva, não o rendimento. O efeito no rendimento precisa ser verificado depois do
  `desvio_clima` por microrregião.
- **Hipótese a investigar:** a defasagem no Cerrado pode refletir o efeito do ENSO no início da
  estação chuvosa (setembro a novembro). Isso pode ser testado separando a safra em subperíodos.

---

## D-04 · Teste de significância por séries substitutas

- **Status:** adotada. A revisão dos níveis de evidência do D-03 foi aprovada em 2026-11-18.
- **Notebook:** `notebooks/eda/eda_enso_defasagens.ipynb` (Parte 3, seção 17)

### Contexto
O D-02 apontou a limitação central da análise de defasagens: o FDR trata as 195 combinações de
defasagem × janela como independentes, quando elas são redundantes, e o ONI é muito autocorrelacionado.
Por isso o FDR ficou conservador demais, e foi preciso um critério de consistência com limites definidos
por nós (2/3 do pico, tolerância de 2 meses).

### Método
- **Hipótese nula:** a chuva da região não tem relação com o ENSO.
- **Estatística:** em cada região, o **maior |ρ| entre as 39 combinações** de defasagem × janela, a mesma
  busca da Parte 2. O teste já desconta a escolha da melhor combinação.
- **Distribuição sob a nula:** a mesma estatística com séries ENSO **substitutas**, que mantêm as
  propriedades do ONI real mas não têm relação com a chuva:

| Família | Nº de séries | Preserva | Não preserva |
|---|---|---|---|
| Randomização de fase (Theiler et al., 1992) | 2.000 | espectro e autocorrelação (1 mês: 0,97; 6 meses: 0,43) | ciclo sazonal da variância do ENSO (no ONI real, a variância de dez–jan é 3,6× a de mai–jun) |
| Deslocamento circular por anos inteiros | 71 | tudo, inclusive o ciclo sazonal | — (mas tem menos resolução) |

- **p-valor:** p = (1 + nº de substitutas com máx|ρ| ≥ observado) / (N + 1).
- **Período:** só as safras da exploração (até 2020).
- **Critério, fixado antes da execução:**
  - **passa:** p < 0,05 nas duas famílias;
  - **indício:** p < 0,05 em apenas uma;
  - **não passa:** nas demais.
- Também foi calculado um p global por divisão (o maior |ρ| entre todas as regiões).

### Resultados
**Biomas:**

| Bioma | máx\|ρ\| (defasagem, janela) | p (fase) | p (deslocamento) | Resultado | p corrigido entre regiões (BH) |
|---|---|---|---|---|---|
| **Cerrado** | −0,29 (7 m, j3) | **0,016** | **0,014** | **passa** | 0,08 / 0,07 |
| Amazônia | −0,35 (3 m, j6) | 0,087 | 0,083 | não passa | 0,22 |
| Pampa | +0,22 (0 m, j1) | 0,19 | 0,19 | não passa | 0,32 |
| Caatinga | −0,22 (3 m, j6) | 0,26 | 0,31 | não passa | 0,33 |
| Mata Atlântica | +0,14 (0 m, j1) | 0,59 | 0,57 | não passa | 0,59 |

**UFs que passam ou têm indício:**

| UF | máx\|ρ\| (defasagem, janela) | p (fase) | p (deslocamento) | Resultado |
|---|---|---|---|---|
| **MT** | −0,41 (7 m, j3) | **0,009** | **0,014** | **passa** |
| **GO** | −0,28 (8 m, j1) | **0,012** | **0,028** | **passa** |
| PA | −0,39 (1 m, j3) | 0,049 | 0,056 | indício |

RS, PR, SC, MS, MG, BA e TO não passam. O p global foi de 0,10 nos biomas e de 0,20 nas UFs.

### Leitura
1. **O Cerrado é o único bioma com relação significativa** depois de descontar a busca e a
   autocorrelação, com cerca de 7 meses de defasagem. Esse resultado é coerente com o MT e o GO, que
   passam individualmente com 7 a 8 meses, e com a repetição no período independente (D-03: −0,28 em
   2021–2025).
2. **A Amazônia não passa** (p ≈ 0,09), embora tenha passado no FDR do índice combinado (D-02). A série
   regional dela tem menos meses válidos e é mais ruidosa, e o teste por substitutas, que respeita a
   autocorrelação, exige um |ρ| maior (limiar de 0,37, contra 0,26 no Cerrado).
3. **O Pampa e o Sul não passam**, apesar do padrão conhecido da literatura. Com cerca de 16 safras, um
   ρ de 0,22 não se distingue do acaso.

### Cautelas
- **Correção entre regiões:** o critério fixado era por região. Corrigindo também para o número de
  regiões testadas (BH), o Cerrado fica em 0,07–0,08 e o MT e o GO em 0,13–0,29. Essa correção foi
  acrescentada **depois** da primeira execução. Por isso, a evidência do Cerrado se apoia em três pilares
  juntos (p ≈ 0,015, repetição em 2021–2025 e coerência com o MT e o GO), e não só no p-valor.
- **O p global** (maior |ρ| entre regiões) é dominado pelas regiões mais ruidosas, que têm limiares mais
  altos. Ele foi mantido como declarado, mas os resultados por região são os principais.
- **A randomização de fase perde o ciclo sazonal do ENSO.** Por isso o critério exige as duas famílias,
  e os resultados delas coincidiram.

### Revisão dos níveis de evidência do D-03 (aprovada)
Substituir o FDR pelo teste por substitutas como critério de evidência **forte**, que é a abordagem mais
adequada para testes redundantes e séries autocorrelacionadas:

| Nível | Critério atual (D-03) | Critério proposto |
|---|---|---|
| forte | candidato + FDR (opção 1 ou 3) + se repete | candidato + **passa no teste por substitutas** + se repete |
| moderada | candidato + se repete | sem mudança |

**Efeito:**

| Região | Nível atual | Nível revisado |
|---|---|---|
| **Cerrado** | moderada | **forte** |
| Amazônia | forte | **moderada** |
| MT | forte | forte |
| GO | moderada | **forte** |
| PA | moderada | moderada (indício) |
| demais | sem mudança | sem mudança |

---

## D-05 · Relação ENSO × chuva por subperíodo da safra

- **Status:** adotada (resultado de análise).
- **Notebook:** `notebooks/eda/eda_enso_defasagens.ipynb` (Parte 3, seção 18)

### Contexto e hipótese
O D-03 levantou a hipótese de que a relação defasada no Cerrado (cerca de 7 meses) viesse do efeito do
ENSO no **início da estação chuvosa**.

### Método
- **(a)** varredura de defasagens em cada subperíodo: início (set–nov), meio (dez–fev) e fim (mar–abr),
  com o teste por substitutas do D-04;
- **(b)** matriz mês da chuva × defasagem do ONI para o Cerrado, o MT e o GO;
- **(c)** checagem acrescentada depois de ver (b): correlação parcial entre o ONI defasado e a chuva,
  controlando o ONI do mesmo mês.
- **Critério fixado antes da execução:** a hipótese é apoiada se, no Cerrado, o máx|ρ| do início for maior
  que o do meio e o do fim **e** o início passar no teste por substitutas.

### Resultados
**(a) Cerrado:**

| Subperíodo | máx\|ρ\| | Defasagem | p (fase) | Resultado |
|---|---|---|---|---|
| início (set–nov) | 0,28 | 6 m | 0,42 | não passa |
| meio (dez–fev) | 0,21 | 8 m | 0,30 | não passa |
| fim (mar–abr) | **0,41** | 9 m | 0,32 | não passa |

**A hipótese não foi apoiada:** o maior |ρ| está no fim da safra, e nenhum subperíodo passa no teste,
porque cada um tem só cerca de 32 a 48 meses.

**(b) A relação muda de sinal ao longo da safra (Cerrado, MT e GO):**
- em **setembro**, a chuva **aumenta** com o ONI do mesmo período (ρ > +0,4 com o ONI de julho a setembro);
- de **dezembro a abril**, a chuva **diminui** com o ONI do verão e do outono anteriores (8 a 12 meses antes).

Por isso a correlação sem defasagem na safra inteira é quase zero: efeitos de sinais opostos se cancelam.

**(c) A relação defasada não é um retrato do estado atual do ENSO:**

| Região | ρ ONI defasado | ρ ONI atual | ρ entre os dois índices | ρ parcial (defasado \| atual) |
|---|---|---|---|---|
| Cerrado (7 m, j3) | −0,29 | −0,02 | +0,21 | −0,30 |
| MT (7 m, j3) | −0,41 | −0,16 | +0,21 | −0,39 |
| GO (8 m, j1) | −0,28 | +0,01 | +0,20 | −0,29 |

Se a relação viesse da alternância de fases (El Niño seguido de La Niña), o ONI defasado seria
negativamente correlacionado com o atual, e a correlação parcial cairia. Nenhuma das duas coisas acontece.

### Conclusão
- A hipótese do início das chuvas **foi descartada** como explicação principal.
- O padrão do Cerrado combina um **efeito simultâneo positivo em setembro** com um **efeito defasado
  negativo de dezembro a abril**. A média da safra inteira esconde essa mudança de sinal.
- **Para as próximas etapas:** no Cerrado, tratar o início da safra (setembro) e o resto separadamente,
  em linha com as fases fenológicas do pipeline.

### Cautelas
- Cada célula da matriz mês × mês tem cerca de 16 safras: ela mostra o padrão, mas não permite afirmar
  significância célula a célula.
- A checagem (c) foi acrescentada depois de ver a matriz (b) e está registrada como tal.

---

## D-06 · Chuva da safra por fase do ENSO

- **Status:** adotada (resultado de análise).
- **Notebook:** `notebooks/eda/eda_enso_defasagens.ipynb` (Parte 3, seção 19)

### Contexto
A correlação supõe uma relação linear e simétrica (o efeito do La Niña como espelho do El Niño). Comparar
as safras por fase é mais fácil de comunicar e permite ver assimetria e efeito da intensidade.

### Escolhas de método
| Escolha | Alternativa | Motivo |
|---|---|---|
| Meses de El Niño/La Niña pela definição da NOAA (ONI ≥ +0,5 / ≤ −0,5 por ≥ 5 meses seguidos) | só o limiar, sem duração | é a definição oficial; evita classificar oscilações curtas como evento |
| Fase da safra: ≥ 4 dos 8 meses (set–abr) na fase | ONI de um trimestre fixo (ex.: NDJ) | usa a mesma janela da safra do pipeline |
| Intensidade pelo pico do \|ONI\| na safra: fraco 0,5–0,9; moderado 1,0–1,4; forte ≥ 1,5 | — | faixas usuais da NOAA |
| Resposta: anomalia da chuva **total** da safra em % da média da microrregião (≥ 7 de 8 meses; ≥ 10 safras para a média) | anomalia padronizada mensal | o total reduz o ruído mensal, e a % é fácil de comunicar |
| Todas as safras (2006–2025) | só a exploração | comparação descritiva, que precisa de todos os eventos |
| Referência: média de todas as safras, e diferença El Niño − La Niña | safras neutras | só 4 safras são neutras (ajuste decidido antes de calcular os resultados) |
| Robusto: IC de 95% (bootstrap) sem cruzar zero **e** p de permutação < 0,05 | — | — |

**Classificação das safras:**
- **El Niño (7):** 2006/07, 2009/10 (forte), 2014/15, 2015/16 (forte), 2018/19, 2019/20 e 2023/24 (forte);
- **La Niña (9):** 2005/06, 2007/08 (forte), 2008/09, 2010/11 (forte), 2011/12, 2017/18, 2020/21, 2021/22 e 2022/23;
- **neutro (4):** 2012/13, 2013/14, 2016/17 e 2024/25.

### Resultados (anomalia da chuva da safra, % da média)
| Bioma | El Niño | La Niña | El Niño − La Niña (p) |
|---|---|---|---|
| **Pampa** | +18,9% [−0,6; +38,0] (p = 0,011) | **−18,4% [−27,5; −11,2] (p = 0,001), robusto** | 37 p.p. (**p = 0,001**) |
| **Amazônia** | −14,4% [−29,9; +0,8] (p = 0,033) | +5,7% | −20 p.p. (**p = 0,041**) |
| Caatinga | −0,6% | +18,0% [−0,9; +36,2] (p = 0,031) | −19 p.p. (p = 0,14) |
| Cerrado | +0,8% | +3,3% | −3 p.p. (p = 0,61) |
| Mata Atlântica | +6,8% | −2,5% | +9 p.p. (p = 0,17) |

**Intensidade** (ρ entre o ONI de pico e a anomalia da safra): Pampa **+0,74**, Amazônia −0,40 e Cerrado −0,19.

### Conclusões
1. **Pampa:** é o efeito mais claro e **simétrico** em termos de chuva, proporcional à intensidade.
   2023/24 (El Niño forte) teve +62%; 2022/23 (La Niña) teve −45%.
2. **Amazônia:** responde sobretudo ao **El Niño** (efeito cerca de 2,5 vezes o do La Niña).
3. **Cerrado:** sem diferença na média por fase, coerente com o D-05 (efeitos opostos ao longo da safra).
   Os **El Niños fortes** (2015/16 e 2023/24) tiveram cerca de 10% menos chuva, e os fracos não. Na
   comparação pela fase da safra **anterior**, o início da safra teve −10,5% depois de El Niño e +13,9%
   depois de La Niña (descritivo, sem teste), o que é coerente com a relação defasada do D-03 e do D-04.

### Por que o Pampa difere do teste por substitutas (D-04)
No D-04, o Pampa não passou (p ≈ 0,19). Aqui o efeito dele é o mais forte. As análises medem coisas
diferentes:
- **o D-04** usa a correlação mês a mês, com ruído mensal grande, só nas safras até 2020;
- **o D-06** usa o total da safra e o contraste entre os extremos, com todas as safras.

O efeito do ENSO no Pampa aparece com clareza **nos eventos**, e não como uma relação linear mês a mês.

### Cautelas
- Poucas safras por fase (7, 9 e 4), e eventos de intensidades muito diferentes dentro da mesma fase.
- Os ICs do El Niño no Pampa e na Amazônia tocam o zero, embora o p da permutação seja menor que 0,05.
  Por isso só o La Niña no Pampa foi classificado como "robusto".

---

## D-07 · Sensibilidade às escolhas de método

- **Status:** adotada (resultado de análise).
- **Notebook:** `notebooks/eda/eda_enso_defasagens.ipynb` (Parte 3, seção 21)

### Contexto
As análises anteriores dependem de escolhas: o tipo de correlação, o tipo de anomalia, o limiar de
completude e a exclusão das estações substitutas. Esta análise verifica se os resultados principais mudam
quando cada escolha é alterada, uma de cada vez.

### Variantes
| Variante | O que muda em relação à base |
|---|---|
| V0 · base | Spearman, anomalia z por mês do calendário, completude de 80%, só estações dentro da microrregião |
| V1 | correlação de Pearson |
| V2 | anomalia mensal em % da média do mês |
| V3 | completude mínima de 70% |
| V4 | completude mínima de 90% |
| V5 | inclui as estações substitutas (91 microrregiões no Cerrado, contra 80) |

### Critérios (fixados antes da execução)
- **Cerrado robusto:** em todas as variantes, mesmo sinal, |ρ(7 m, j3)| ≥ 0,20, melhor defasagem entre 5 e
  9 meses e p (fase) < 0,10.
- **Fases robustas:** mesmo sinal, com magnitude ≥ 50% da base (só V3, V4 e V5, que alteram o total da safra).

### Resultados
**Cerrado (exploração, safras até 2020):**

| Variante | ρ (7 m, j3) | Melhor combinação | p fase / deslocamento |
|---|---|---|---|
| V0 · base | −0,294 | 7 m, j3 | 0,016 / 0,014 |
| V1 · Pearson | −0,281 | 7 m, j1 | 0,013 / 0,028 |
| V2 · anomalia % | −0,282 | 8 m, j1 | 0,033 / 0,042 |
| V3 · completude 70% | −0,291 | 7 m, j3 | 0,018 / 0,014 |
| V4 · completude 90% | −0,284 | 7 m, j3 | 0,017 / 0,014 |
| V5 · com substitutas | −0,291 | 8 m, j1 | 0,018 / 0,014 |

**Fases (anomalia da chuva da safra, %):**

| Variante | Pampa · La Niña | Pampa · El Niño | Amazônia · El Niño |
|---|---|---|---|
| V0 · base | −18,4 | +18,9 | −14,4 |
| V3 · completude 70% | −18,4 | +19,6 | −13,6 |
| V4 · completude 90% | −17,6 | +18,6 | −13,8 |
| V5 · com substitutas | −18,4 | +18,9 | −9,4 |

### Conclusão
- **O Cerrado é robusto em todas as variantes:** a defasagem fica sempre entre 7 e 8 meses, e o p continua
  abaixo de 0,05 nas duas famílias de séries substitutas.
- **As fases são robustas:** o Pampa praticamente não muda (não há microrregiões com soja que dependam de
  estações substitutas). Na Amazônia, o efeito do El Niño se atenua com as substitutas (−9,4%), mas continua
  acima de 50% da base.
- Os sinais dos outros biomas não mudam em nenhuma variante.
- **As escolhas de método feitas nas análises (D-01 a D-06) não determinam os resultados principais.**

### Correção feita durante a análise
Na primeira execução, a V5 deu resultados idênticos à base nas fases, porque a função de agregação filtrava
pelas microrregiões da base. A função passou a usar as microrregiões de cada variante; os resultados das
seções anteriores não mudaram.

---

## D-08 · Outras variáveis climáticas e o ENSO

- **Status:** adotada (resultado de análise).
- **Notebook:** `notebooks/eda/eda_enso_defasagens.ipynb` (Parte 3, seção 22)

### Contexto
O ENSO pode afetar a soja por outros caminhos além do total de chuva: a distribuição da chuva (dias secos e
veranicos), o calor e a data de início da estação chuvosa, que define a janela de plantio.

### Variáveis e escolhas
| Variável | Escala | Definição | Por quê |
|---|---|---|---|
| fração de dias secos | mensal | dias com < 2 mm ÷ dias com dado | mede a distribuição da chuva, e não só o total |
| Tmax média | mensal | média da temperatura máxima diária | calor durante a safra |
| fração de dias quentes | mensal e safra | dias com Tmax acima do **P90 da própria estação** (set–abr) | a Tmax do pipeline é o máximo das médias horárias e fica subestimada (mediana de 29,8 °C); um limite relativo não é afetado por esse viés, ao contrário de um fixo como 35 °C |
| maior veranico | safra | maior sequência de dias secos de 1/dez a 31/mar | período de floração e enchimento de grãos |
| início das chuvas | safra | primeiro dia após 1/set com ≥ 20 mm em 3 dias **sem** 10 dias secos seguidos nos 30 dias seguintes | critério clássico; validado (mediana em **14/out** no Centro-Oeste) |

**O início das chuvas é analisado só no Cerrado, na Amazônia, no MT e no GO,** onde há estação chuvosa
definida. No Sul, o critério dá 10/set, porque lá não há estação chuvosa definida e ele só pega a primeira chuva.

### Testes (fixados antes da execução)
- **Mensais:** varredura de defasagens e teste por séries substitutas (D-04), safras até 2020.
- **Por safra:** comparação por fases (D-06) e correlação de Spearman com o ONI de pico e com o ONI médio de
  mai–jul antes da safra, com p por permutação. Robusto se p < 0,05. Todas as safras (2006–2025).

### Checagens acrescentadas depois da primeira execução
1. **Tendência:** a temperatura sobe ao longo dos anos, e o ONI também teve tendência de alta entre 2004 e
   2020 (correlação de +0,20 com o tempo). Duas séries com tendência se correlacionam mesmo sem relação causal,
   e as séries substitutas não reproduzem esse alinhamento. **O teste foi refeito com a temperatura sem a
   tendência linear** de cada microrregião.
2. **Correção FDR (Benjamini–Hochberg)** sobre os 69 p-valores das variáveis por safra (23 linhas × 3 testes).
   Com tantos testes, uns 3 ou 4 dariam p < 0,05 só por acaso.

### Resultados
**Mensais (teste por substitutas):**

| Variável | Cerrado | Amazônia | Caatinga | Mata Atlântica | Pampa |
|---|---|---|---|---|---|
| fração de dias secos | **passa** (ρ = +0,32; 7 m) | **passa** (+0,41; 3 m) | não | não | não |
| Tmax média (com tendência) | passa (+0,50) | passa (+0,57) | passa (+0,46) | passa (+0,34) | não |
| **Tmax média, sem tendência** | **passa** (+0,39) | **passa** (+0,43) | **passa** (+0,42) | não | não |
| fração de dias quentes (com tendência) | passa | passa | passa | passa | não |
| **fração de dias quentes, sem tendência** | não | não | indício | não | não |

**Por safra:** **nenhum resultado se sustenta após a correção FDR** (o menor p corrigido é 0,36). Os p < 0,05
isolados (início das chuvas mais tardio na Amazônia depois de El Niño antecedente, ρ = +0,52; dias quentes no
Cerrado, ρ = +0,50) ficam como **indícios**. O maior veranico não mostra relação com o ENSO em nenhuma região.

### Conclusões
1. **Os dias secos confirmam o resultado principal:** no Cerrado, mais dias secos se relacionam com o ENSO de
   **7 meses antes**, a mesma defasagem encontrada com a chuva. É uma confirmação independente, com outra variável.
2. **Temperatura:** o El Niño se relaciona com **mais calor** no Norte e no Centro-Oeste (3 a 5 meses de
   defasagem), e o sinal resiste à remoção da tendência. É o sinal mais forte entre as variáveis testadas.
3. **O sinal dos dias quentes vinha, em grande parte, da tendência de aquecimento**, e não do ENSO. Sem a
   checagem de tendência, essa conclusão estaria errada.
4. **No Pampa,** nenhuma variável mensal passa, coerente com o D-04 e o D-06 (no Sul, o efeito aparece nos eventos).
5. **As variáveis por safra** (veranico, início das chuvas, dias quentes) não têm evidência robusta com cerca de 20 safras.

### Cautelas
- A Tmax do pipeline é subestimada. Isso não afeta as anomalias, que comparam cada estação com ela mesma, mas os
  valores absolutos não devem ser interpretados.
- A remoção de tendência linear é uma aproximação; a tendência pode não ser linear.
- As duas checagens foram decididas depois da primeira execução e estão registradas como tal.

---

## D-09 · Série longa de rendimento (PAM 1974–2025): dados e método

- **Status:** adotada.
- **Notebook:** `notebooks/eda/eda_enso_rendimento.ipynb` (seções 1 a 3)

### Contexto
As análises do D-01 ao D-08 usam a chuva das estações (safras 2005–2026, cerca de 20 safras). Para ver se o ENSO
aparece **no próprio rendimento**, é preciso uma série bem mais longa: com 20 safras, só correlações muito fortes
seriam detectáveis.

### Opções consideradas
| Opção | Período | Por que sim / por que não |
|---|---|---|
| Base de modelagem do projeto | 2000–2025 | já pronta, mas curta e depende do `desvio_clima` nacional |
| PAM por microrregião (nível n9 do SIDRA) | 1990–2025 | oficial, mas o SIDRA só tem esse nível a partir de 1990 |
| **PAM por município, agregada por microrregião** | **1974–2025** | **escolhida:** 51 safras, mesma agregação do pipeline |

### Escolhas e evidência
- **Agregação:** município → microrregião pelo centróide, na malha de 2020 (mesmo método do pipeline). Na validação
  contra a série oficial por microrregião (1990–2025), a produção **coincide em 99,98% em média** (mínimo 99,41%,
  em 2025). Só 0,036% da produção fica sem microrregião.
- **Filtros:** área colhida ≥ 100 ha, rendimento ≤ 6.000 kg/ha (os mesmos da base de modelagem) e pelo menos 15 anos
  por microrregião (261 microrregiões).
- **Tendência tecnológica: LOWESS robusto, janela de 25 anos, por microrregião.** A primeira versão usava 15 anos e
  foi **revista depois da primeira execução**: a tendência flexível dobrava para baixo nas secas de 2020–2023 (La Niña)
  e absorvia o próprio efeito climático (Pampa 2021–2023: −4% com 15 anos, −15% com 25 anos). Princípio adotado: a
  tendência tem de ser bem mais lenta que o ciclo do ENSO (2 a 7 anos) e pouco sensível a anos extremos.
- **Sensibilidade da tendência** (LOWESS 15 anos, mediana móvel de 9 anos, polinômio de grau 2): fora a Caatinga, a
  correlação entre as anomalias por bioma é ≥ 0,91.
- **Teste (fixado antes da execução):** perfil de 16 janelas do ONI de 3 meses (de jan(t−1) a abr(t), sendo t o ano
  da colheita). O máximo |ρ| entre as janelas é comparado com séries ONI substitutas, como no D-04 (2.000
  randomizações de fase e deslocamentos circulares por anos inteiros). **Passa** se p < 0,05 nas duas famílias,
  **indício** se em uma.
- **Fases:** mesma classificação do D-06, com IC por bootstrap e teste de permutação para a diferença El Niño − La Niña.

### Acréscimos depois da primeira execução (registrados como tal)
- **3b. Teste por UF** (12 principais produtoras): previsto no D-01 como divisão de sensibilidade.
- **5b. Período recente (2000–2025):** acrescentado depois de ver a tabela de estabilidade; é **exploratório**.

### Limitações
- Antes de 1990, os desmembramentos de municípios não podem ser validados. Por isso a análise principal é por
  bioma, e a **Caatinga** (poucas microrregiões e safras, tendência instável) não deve ser interpretada.
- A tendência usa a série inteira (análise descritiva). Para modelagem, ela deve ser ajustada só com os anos de treino.
- A composição dos biomas muda ao longo do tempo: o Cerrado passa de 4% da produção nacional em 1975 para 55% hoje.

---

## D-10 · ENSO × rendimento da soja: resultados

- **Status:** adotada (resultado de análise).
- **Notebook:** `notebooks/eda/eda_enso_rendimento.ipynb` (seções 3 a 6)

### Resultados na série inteira (safras 1975–2025)
| Região | Janela de máx\|ρ\| | ρ | p (fase / deslocamento) | Resultado |
|---|---|---|---|---|
| PI | dez(t−1) | −0,59 | 0,004 / 0,014 | **passa** |
| MA | abr(t) | −0,52 | 0,006 / 0,014 | **passa** |
| MT | jan(t) | −0,36 | 0,025 / 0,069 | indício |
| Amazônia | abr(t) | −0,32 | 0,057 / 0,097 | não passa (quase) |
| Cerrado | dez(t−1) | −0,31 | 0,134 / 0,153 | não passa |
| Pampa, RS, PR | fev(t) / mai(t−1) | ≈ +0,18 | > 0,3 | não passa |
| Mata Atlântica | mai(t−1) | ≈ 0 | > 0,9 | sem relação |

Com a correção FDR sobre as 12 UFs testadas, o p de PI e MA fica em torno de 0,04.

**Fases:** no MT, La Niña **+4,2% (robusto)**, El Niño −3,0% e diferença El Niño − La Niña de −7 p.p. (p = 0,01).
No Cerrado, a diferença vai no mesmo sentido (−4,3 p.p., p = 0,09). No Pampa, El Niño − La Niña = +7 p.p., sem
significância.

### Estabilidade
- **Cerrado:** ρ ≈ 0 em 1975–1999 e ρ = −0,58 em 2000–2025. No período recente (exploratório), Cerrado (ρ = −0,59)
  e MT (ρ = −0,56) teriam p < 0,05 nas duas famílias.
- A mudança é coerente com a expansão da soja no Cerrado e com a melhor qualidade dos dados municipais recentes.

### Conclusões
1. **Centro-Norte (MATOPIBA, MT, Amazônia):** o El Niño se relaciona com **rendimento menor**, com o ONI de dezembro
   a abril da safra. É coerente com a chuva (El Niño mais seco no Norte, D-06) e com a defasagem de 7 meses do
   Cerrado (D-03, D-04), que aqui aparece como relação com o ONI do fim do ano anterior.
2. **Sul (Pampa, RS, PR):** a chuva responde aos eventos (D-06), mas o **rendimento responde pouco** ao ENSO. Muitas
   quebras de safra no Sul ocorreram em anos neutros. Hipótese: importa **quando** a seca acontece (floração e
   enchimento de grãos), e não só o total da safra.
3. O sinal no Cerrado é **recente** (2000+). Para a modelagem, o período recente é o mais representativo.

### Cautelas
- As correlações são moderadas (|ρ| entre 0,3 e 0,6): o ENSO explica só parte da variação do rendimento.
- O resultado do período recente é exploratório: o período foi escolhido depois de ver os dados.

---

## D-11 · Cadeia ENSO → chuva → rendimento: desenho da análise

- **Status:** adotada.
- **Notebook:** `notebooks/eda/eda_enso_cadeia.ipynb` (seções 1 a 3)

### Contexto
Os D-01 a D-08 tratam do elo ENSO → chuva, e o D-10 do elo ENSO → rendimento. Faltava ver se a relação com o
rendimento **passa pela chuva**, e explicar por que, no Sul, a chuva responde ao ENSO e o rendimento não.

### Escolhas (fixadas antes da execução)
| Item | Escolha | Por quê, e não a alternativa |
|---|---|---|
| ENSO | ONI médio set(t−1)–abr(t) | é a janela da safra e das fases (D-06). A janela de máx\|ρ\| do D-10 foi escolhida olhando os dados e não foi reaproveitada |
| Chuva | anomalia % do total por microrregião: safra (≥ 7 de 8 meses), início (set–nov), meio (dez–fev) e fim (mar–abr) | mesma chuva e mesmos subperíodos do D-05 |
| Rendimento | anomalia à tendência LOWESS de 25 anos por microrregião (D-09) | tendência estimada nos 50 anos, mais estável que só em 2006–2025 |
| Unidade | painel microrregião × safra (2006–2025), microrregiões com ≥ 10 safras (153) | cada microrregião é comparada com ela mesma, e o painel usa toda a variação local |
| Regiões | bioma (D-01) e, como sensibilidade, as UFs MT, GO, PR, RS e o MATOPIBA (MA + PI) | as regiões com resultados mais claros no D-10 |
| Significância | permutação das **safras em bloco** (5.000) e bootstrap das safras (2.000), FDR por tabela | as microrregiões de um mesmo ano não são independentes; permutar microrregião × safra soltas daria p pequeno demais |
| Cadeia | ρ total (ONI, rend.) × ρ parcial (ONI, rend. \| chuva); fração = 1 − parcial ÷ total | só é interpretada se os três elos tiverem p < 0,05 |
| Hipótese do Sul | ρ(chuva dez–fev, rend.) > ρ(chuva safra, rend.) no Pampa, RS e PR | hipótese do D-10, escrita antes de rodar |

### Acréscimo depois da primeira execução (registrado como tal)
- **7c. Cadeia no nível regional:** na primeira execução, chuva → rendimento foi bem mais forte nas médias regionais
  do que no painel (MATOPIBA: 0,74 contra 0,14). Isso indica **erro de medida** da chuva da microrregião (uma ou
  duas estações), que puxa a fração "pela chuva" para zero. A cadeia foi refeita com as médias regionais. É exploratória.

### Limitações
- Só 20 safras; a cobertura por estações é baixa no PR (45% da área), na Mata Atlântica (56%) e na Amazônia (59%).
- A Caatinga tem 1 microrregião: não é interpretada.
- A correlação parcial é descritiva: não prova o mecanismo.

---

## D-12 · Cadeia ENSO → chuva → rendimento: resultados

- **Status:** adotada (resultado de análise).
- **Notebook:** `notebooks/eda/eda_enso_cadeia.ipynb` (seções 3 a 8)

### Resultados
| Região | ENSO → chuva (safra; set–nov) | chuva dez–fev → rend. | ENSO → rend. (painel; regional) | fração pela chuva (painel; regional) |
|---|---|---|---|---|
| Pampa | +0,59 **conf.**; +0,64 **conf.** | +0,45 **conf.** | −0,05; +0,24 | não interpretável (total ≈ 0) |
| RS | +0,56 **conf.**; +0,63 **conf.** | +0,47 **conf.** | +0,05; +0,27 | não interpretável |
| PR | +0,25; +0,35 indício | +0,31 **conf.** | +0,06; +0,02 | não interpretável |
| Cerrado | −0,07; +0,05 | +0,16 **conf.** | **−0,32**; **−0,52** | 0,01 [−0,03; +0,08]; −0,02 |
| MT | −0,11; +0,05 | +0,03 | **−0,44**; **−0,55** | 0,01 [−0,05; +0,06]; 0,04 |
| GO | −0,20; −0,01 | +0,19 indício | **−0,30**; **−0,48** | 0,04; −0,19 |
| MATOPIBA (MA + PI) | −0,18; −0,31 | +0,08 | **−0,46**; **−0,76** | 0,03; 0,01 |
| Mata Atlântica | +0,23 indício; +0,42 **conf.** | +0,29 **conf.** | +0,04; +0,28 | não interpretável |

Pela regra fixada, a cadeia **não fica estabelecida em nenhuma região**: em nenhuma delas os três elos são
significativos ao mesmo tempo.

### Conclusões
1. **A chuva que importa para o rendimento é a de dez–fev** (floração e enchimento de grãos), em todas as regiões
   onde a chuva se relaciona com o rendimento. No Pampa, a relação não é linear: chuva bem acima da média não
   aumenta o rendimento.
2. **Sul: a hipótese do D-10 foi confirmada.** A chuva de dez–fev se relaciona mais com o rendimento do que a da
   safra inteira (Pampa: diferença +0,25, IC de +0,07 a +0,42; RS e PR também). O ENSO age sobretudo na chuva de
   set–nov, que não afeta o rendimento, e o excesso de chuva do El Niño não ajuda. Todas as grandes quebras do Pampa
   (2012, 2020, 2022, 2023, 2025) tiveram dez–fev seco, em La Niña, El Niño fraco ou safra neutra.
3. **Centro-Norte: o ENSO se relaciona com o rendimento por outro caminho além da chuva total.** A relação ENSO ×
   rendimento é forte, mas quase nada dela é acompanhado pela chuva medida, nem no painel nem no nível regional, com
   a chuva da safra ou de dez–fev. Os candidatos são o calor (D-08), a distribuição da chuva e a radiação. Não foi testado.
4. No Pampa, depois de considerar a chuva, o El Niño fica associado a um rendimento um pouco menor (ρ parcial
   ≈ −0,2). É coerente com o excesso de chuva e de nebulosidade, mas é exploratório.

### Implicações
- **Sul:** usar a **chuva de dez–fev** como variável climática principal; o índice ENSO sozinho informa pouco.
- **Centro-Norte:** o ENSO carrega informação que a chuva das estações não carrega. O próximo teste é a **temperatura**
  como caminho.

---

## Modelo para novas decisões

```markdown
## D-XX · Título curto

- **Status:** proposta | adotada | provisória | substituída por D-YY
- **Notebook/código:** caminho

### Contexto
O problema e por que ele precisa de uma decisão.

### Opções consideradas
Tabela ou lista das alternativas.

### Evidência
Números, figuras e testes que sustentam a escolha.

### Decisão
A escolha, em uma frase.

### Por quê
A justificativa de cada opção escolhida ou descartada.

### Consequências e limitações
O que muda, o que fica de fora e quando reavaliar.
```

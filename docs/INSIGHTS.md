# Insights — Área de Crédito

> Desafio técnico MYDE — Analista de Dados  
> **Participante:** Lucas Almeida Gonçalves  
> **Notion:** [Hub MYDE](https://app.notion.com/p/38f5aecd550381b4a587caa909fc7445)  
> **Moeda:** coroa tcheca (CZK, Kč) — dataset Berka/PKDD'99 (República Tcheca, anos 90)

---

## Resumo executivo (direção para a diretoria)

A carteira de **682 empréstimos** apresenta **saúde relativa** (88,86% sem problemas graves), mas o risco **não é homogêneo**: concentra-se em contas **sem cartão**, na **faixa intermediária de valor** e em **regiões com menor renda e maior desemprego**. A taxa global de inadimplência (**11,14%**) é aceitável para monitoramento, porém **4,7× maior** entre clientes sem cartão do que entre os com cartão.

**Direção recomendada:** tratar inadimplência como problema de **segmentação e política de concessão**, não apenas de cobrança. O dashboard Power BI (`powerbi/desafio-analista-de-dados-myde-lucas-a-goncalves.pbix`) foi desenhado para acompanhamento contínuo por região, status e faixa de valor.

---

## Análise estratégica de negócio

### 1. Saúde da carteira vs. exposição ao risco

| Indicador | Valor | Leitura de negócio |
|---|---|---|
| Total de empréstimos | 682 | Base analítica pequena, típica de banco regional — decisões devem considerar **amostra por distrito** (~9 empréstimos/distrito em média) |
| Status A + C (sem problema grave) | 606 (88,86%) | Carteira majoritariamente performando |
| Status B + D (inadimplência) | 76 (11,14%) | **1 em cada 9** empréstimos com problema — nível que exige política ativa, não alarmismo |
| Empréstimos em andamento com débito (D) | 45 | Risco **operacional imediato** — priorizar renegociação antes de virar B |

**Implicação estratégica:** o banco não enfrenta crise sistêmica de crédito, mas tem **cauda de risco identificável** que pode ser endereçada com regras de concessão e monitoramento segmentado.

---

### 2. Segmentação por produto — cartão como proxy de perfil

| Grupo | Empréstimos | Taxa inadimplência |
|---|---|---|
| **Com cartão** | 476 | **2,94%** |
| **Sem cartão** | 206 | **13,87%** |

**Hipótese de negócio:** a posse de cartão pode indicar relacionamento mais maduro com o banco, histórico de pagamento ou perfil de renda — não necessariamente causalidade. Ainda assim, a **lacuna de 10,9 p.p.** é material.

**Implicação estratégica:**
- Contas **sem cartão** devem ser tratadas como **segmento de risco elevado** na concessão de novos empréstimos.
- Oferta de cartão ou produtos de relacionamento pode ser **caminho de retenção**, mas só após validar capacidade de pagamento (evitar concessão automática só pelo indicador).

---

### 3. Segmentação por ticket — onde a política de limites falha

| Faixa (CZK) | Qtd | Taxa inadimplência |
|---|---|---|
| Pequeno (< 50k) | 126 | **3,97%** |
| Médio (50k–150k) | 269 | **9,67%** |
| Grande (> 150k) | 287 | **15,68%** |

**Implicação estratégica:** o risco **cresce com o ticket** — especialmente na faixa Média e Grande. Isso sugere que o scoring atual pode ser adequado para microcrédito, mas **insuficiente para valores intermediários e altos**, onde a exposição financeira por inadimplência é maior.

**Ação de negócio:** revisar limites e exigir critérios adicionais (renda, saldo médio, histórico de transações) acima de 50k CZK.

---

### 4. Risco regional — variáveis macro no `dim_district`

A query 6 (SQL) cruza inadimplência com **salário médio (A11)** e **desemprego (A12/A13)** por distrito. Padrão observado:

- Distritos com **menor salário médio** e **maior desemprego** tendem a **taxas mais altas** de inadimplência.
- **32 de 77** distritos com empréstimos têm **0%** de inadimplência (nenhum B/D) — oportunidade de **expansão controlada** nessas regiões.
- Distritos com poucos empréstimos exibem taxas voláteis (0%, 25%, 50%) — **não usar isoladamente** para decisão; combinar com volume mínimo.

**Implicação estratégica:** incorporar **variáveis macro-regionais** no motor de crédito (scoring ou limites por distrito), alinhado ao que o banco já tem em `district`.

---

### 5. Capacidade preditiva (Python) — o que o modelo permite e o que não permite

| Métrica | Valor | Leitura |
|---|---|---|
| AUC (regressão logística) | **0,682** | Discriminação **moderada** — útil para **priorizar** revisão manual |
| Uso recomendado | Triagem | **Não** substituir analista em decisão final |

**Implicação estratégica:** o modelo suporta uma **fila de trabalho** (quais empréstimos revisar primeiro), mas não automatização cega de aprovação/negação.

---

### 6. Como o painel executivo responde às perguntas de negócio

| Pergunta da diretoria | Onde ver no Power BI |
|---|---|
| Como está a carteira hoje? | Página **Visão Geral** — KPIs valor total, inadimplência, qtd empréstimos |
| A inadimplência piora no tempo? | Gráfico de **concessões** + slicer de **Ano** |
| Quais regiões concentram risco? | Página **Risco por Região** — barras por distrito |
| Onde agir primeiro? | Ranking por **taxa** e por **volume** + tabela `fact_agg_carteira` |
| Como está um status/faixa específico? | Slicers de **status** e **faixa_valor** |

---

## Recomendações práticas e acionáveis

### Curto prazo (0–30 dias) — operação e cobrança

| # | Ação | Responsável sugerido | Métrica de sucesso | Evidência |
|---|---|---|---|---|
| 1 | Priorizar cobrança/renegociação dos **45 empréstimos status D** (em débito, em andamento) | Cobrança / Crédito | Redução de D→B nos próximos ciclos | Query 2 — status D=45 |
| 2 | Instituir **revisão semanal** do KPI **Taxa Inadimplência** no painel (meta: manter ≤ 12%) | Gestão de Crédito | KPI estável ou em queda | PBI — Visão Geral |
| 3 | Listar contas **sem cartão** com empréstimo ativo (status C ou D) para contato proativo | Relacionamento | Lista semanal de contas em risco | Query 9 — 13,87% no segmento |

---

### Médio prazo (1–3 meses) — política de crédito

| # | Ação | Responsável sugerido | Métrica de sucesso | Evidência |
|---|---|---|---|---|
| 4 | Exigir **critérios reforçados** para empréstimos **≥ 50k CZK** (comprovação de renda, saldo médio acima da média do distrito) | Política de Crédito | Queda da taxa na faixa Média (hoje 9,67%) | Query 5 + Query 8 |
| 5 | Incorporar **score regional** (salário A11, desemprego A12/A13) no comitê de aprovação | Risco / Modelagem | Mapa de calor por distrito no painel | Query 6 + PBI Risco por Região |
| 6 | Piloto de **oferta de cartão** para bons pagadores sem cartão (status A/C, sem histórico B/D) — medir inadimplência em 6 meses | Produtos / CRM | Taxa do segmento “sem cartão” converge para < 10% | Query 9 |

---

### Médio prazo — analytics e governança

| # | Ação | Responsável sugerido | Métrica de sucesso | Evidência |
|---|---|---|---|---|
| 7 | Usar modelo Python (AUC 0,68) como **fila de priorização** de análise manual, não decisão automática | Data / Risco | % de B/D capturados no top 20% do score | `analise_risco.ipynb` |
| 8 | Definir **volume mínimo** (ex.: ≥ 5 empréstimos) antes de decisões por distrito no painel | Gestão + BI | Menos distritos com 0%/100% isolados | Análise regional — amostra pequena |
| 9 | Revisão mensal do comitê com **3 cortes**: região × faixa × cartão | Diretoria de Crédito | Ata com metas por segmento | Dashboard completo |

---

### O que **não** recomendo (evitar armadilhas)

- **Não** negar automaticamente todo cliente sem cartão — o indicador é associativo, não causal.
- **Não** usar a coluna `taxa_inadimplencia_pct` da tabela agregada linha a linha como KPI global (grain inclui status; ver `docs/TROUBLESHOOTING.md`).
- **Não** expandir agressivamente em distritos com alta inadimplência histórica sem piloto controlado.

---

## Síntese para o avaliador

| Critério MYDE | Onde está na entrega |
|---|---|
| Estruturação correta dos dados (SQL) | `sql/consultas.sql` + `sql/views/` (star schema) |
| **Análise estratégica de negócio** | **Este documento — seções acima** |
| Dashboard executivo claro | `powerbi/*.pbix` — 3 páginas, KPIs, filtros |
| **Recomendações práticas e acionáveis** | **Tabelas de ações com responsável e métrica** |
| Coerência e clareza | Métricas alinhadas SQL ↔ PBI ↔ Python (11,14%, 682, AUC 0,682) |

---

## Entregáveis

| Parte | Artefato |
|---|---|
| SQL | `sql/consultas.sql` + views em `sql/views/` |
| Power BI | `powerbi/desafio-analista-de-dados-myde-lucas-a-goncalves.pbix` |
| Python (bônus) | `python/analise_risco.ipynb` |
| Documentação | `README.md`, `docs/*` |

**Repositório:** https://github.com/lucasagon/myde-desafio-tecnico-analista-de-dados-lucas-a-goncalves  
**Notion:** https://app.notion.com/p/38f5aecd550381b4a587caa909fc7445

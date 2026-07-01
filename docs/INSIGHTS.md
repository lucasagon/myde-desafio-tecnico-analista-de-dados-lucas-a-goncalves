# Insights — Área de Crédito

> Desafio técnico MYDE — Analista de Dados  
> Participante: Lucas Almeida Gonçalves  
> **Notion:** [Hub MYDE](https://app.notion.com/p/38f5aecd550381b4a587caa909fc7445)  
> Moeda do dataset: **coroa tcheca (CZK, Kč)** — base Berka/PKDD'99 (República Tcheca, anos 90)

## Principais achados

1. **Taxa geral de inadimplência: 11,14%** (76 de 682 empréstimos com status B ou D). A carteira é majoritariamente saudável (C=403, A=203), mas o risco concentrado em B/D merece monitoramento ativo.

2. **Cartão de crédito associado a menor inadimplência:** contas com cartão apresentam **2,94%** de inadimplência vs **13,87%** sem cartão. Pode refletir perfil mais estável ou acesso a crédito rotativo — recomenda-se cruzar com renda/saldo antes de políticas automáticas.

3. **Faixa de valor importa:** empréstimos **Médios** (50k–150k CZK) têm maior taxa de inadimplência (**9,67%**) que Pequenos (**3,97%**), sugerindo revisão de limites e scoring na faixa intermediária.

4. **Risco regional heterogêneo:** distritos com menor salário médio (A11) e maior desemprego (A12/A13) tendem a taxas mais altas — políticas de crédito podem incorporar variáveis macro regionais do `dim_district`.

5. **Modelo preditivo (Python):** regressão logística com AUC **0,68** — sinal preditivo moderado. Útil para priorização, não para decisão automática isolada.

## Recomendações

- Monitorar KPI de inadimplência por região e faixa de valor no dashboard Power BI (`fact_agg_carteira`).
- Avaliar política diferenciada para contas sem cartão (maior risco observado).
- Reforçar análise de saldo médio (query 8: 2.073 contas acima da média do distrito) como indicador complementar.
- Revisar concessões na faixa Média com critérios adicionais de capacidade de pagamento.

## Entregáveis

| Parte | Artefato |
|---|---|
| SQL | `sql/consultas.sql` + views em `sql/views/` |
| Power BI | `powerbi/desafio-analista-de-dados-myde-lucas-a-goncalves.pbix` (+ `.pbit` template) |
| Python (bônus) | `python/analise_risco.ipynb` |
| Documentação | `README.md`, `docs/*` (incl. `RUNBOOK.md`, `TROUBLESHOOTING.md`, `ENTREGA.md`) |

Repositório: https://github.com/lucasagon/myde-desafio-tecnico-analista-de-dados-lucas-a-goncalves  
Notion: https://app.notion.com/p/38f5aecd550381b4a587caa909fc7445

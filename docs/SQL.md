# Parte 1 — SQL

**Notion:** [Hub MYDE](https://app.notion.com/p/38f5aecd550381b4a587caa909fc7445) · **Runbook:** [`RUNBOOK.md`](RUNBOOK.md)

## Consultas analíticas (`sql/consultas.sql`)

| # | Questão | Resultado-chave (validado) |
|---|---|---|
| 1 | Contas por região | 77 distritos; maior concentração em Praga |
| 2 | Carteira por status | A=203, B=31, C=403, D=45 empréstimos |
| 3 | Taxa de inadimplência | **11,14%** (76 de 682 empréstimos B/D) |
| 4 | Top 10 saldos | Última transação por conta via `ROW_NUMBER()` |
| 5 | Faixas de valor | Taxa de inadimplência por Pequeno/Médio/Grande |
| 6 | Risco × região | Correlação salário/desemprego vs inadimplência |
| 7 | Ranking regional | `RANK() OVER (PARTITION BY district_id)` |
| 8 | Saldo acima da média | CTE com média por distrito |
| 9 | Cartão × risco | Comparação inadimplência com/sem cartão |

## Star schema (`sql/views/`)

### Dimensões

| View | PK | Linhas | FKs |
|---|---|---|---|
| `vw_dim_district` | district_id | 77 | — |
| `vw_dim_client` | client_id | 5.369 | district_id |
| `vw_dim_account` | account_id | 4.500 | district_id |
| `vw_dim_disp` | disp_id | 5.369 | client_id, account_id |
| `vw_dim_card` | card_id | 892 | disp_id |

### Fatos

| View | Grain | Linhas | FKs |
|---|---|---|---|
| `vw_fact_loan` | empréstimo | 682 | account_id, district_id, loan_date |
| `vw_fact_trans` | transação | 1.056.320 | account_id, trans_date |
| `vw_fact_card_account` | conta | 4.500 | account_id, card_id (nullable) |
| `vw_fact_agg_carteira` | região×mês×status×faixa | 648 | district_id, periodo_mes, status |

### Colunas derivadas no SQL

- `status_grupo`: bom (A/C) | mau (B/D)
- `faixa_valor`: Pequeno (<50k) | Médio | Grande (>150k)
- `possui_cartao`: flag 0/1
- `idade_cliente`: `TIMESTAMPDIFF` em `dim_client`

### Relacionamentos Power BI (FK)

Ver `docs/POWERBI.md` para mapeamento dim → fato.

## Validação

```bash
python python/validate_sql.py
```

Todas as views retornam dados sem erro no MariaDB público.

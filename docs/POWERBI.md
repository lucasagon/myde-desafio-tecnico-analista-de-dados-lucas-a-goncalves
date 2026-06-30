# Parte 2 — Power BI

Arquivo alvo: `powerbi/carteira_credito.pbix`

## Abordagem SQL-first (star schema)

1. Importar views de `sql/views/` via **Native Query** (ou CSVs em `powerbi/data/` gerados por `python powerbi/export_views.py`)
2. Desativar detecção automática de relacionamentos
3. Relacionar dim → fato por FKs
4. Criar tabela `Calendario` e medidas DAX

## Tabelas do modelo

| Tabela PBI | Origem | Linhas |
|---|---|---|
| dim_district | vw_dim_district | 77 |
| dim_client | vw_dim_client | 5.369 |
| dim_account | vw_dim_account | 4.500 |
| dim_disp | vw_dim_disp | 5.369 |
| dim_card | vw_dim_card | 892 |
| fact_loan | vw_fact_loan | 682 |
| fact_trans | vw_fact_trans | 1.056.320 |
| fact_card_account | vw_fact_card_account | 4.500 |
| fact_agg_carteira | vw_fact_agg_carteira | 648 |
| Calendario | DAX `CALENDAR` | — |

## Relacionamentos (1:N, single direction)

| De | Para | Coluna |
|---|---|---|
| fact_loan | dim_district | district_id |
| fact_loan | dim_account | account_id |
| fact_loan | Calendario | loan_date → Date |
| fact_trans | dim_account | account_id |
| fact_trans | Calendario | trans_date → Date |
| fact_card_account | dim_account | account_id |
| fact_card_account | dim_card | card_id |
| fact_agg_carteira | dim_district | district_id |
| dim_client | dim_district | district_id |
| dim_disp | dim_client | client_id |
| dim_disp | dim_account | account_id |
| dim_card | dim_disp | disp_id |

## Tabela Calendário (DAX)

```dax
Calendario = ADDCOLUMNS(
    CALENDAR(DATE(1993,1,1), DATE(1998,12,31)),
    "Ano", YEAR([Date]),
    "Mes", MONTH([Date]),
    "AnoMes", FORMAT([Date], "YYYY-MM")
)
```

## Medidas DAX

Ver `powerbi/medidas.dax` — principais:

- Valor Total Emprestado, Ticket Médio, Taxa Inadimplência (11,14% baseline)
- Qtd Contas, Clientes, Cartões
- Concessões e valor no período (via Calendário)

## Página 1 — Visão Geral da Carteira

- **KPIs:** Valor Total Emprestado | Taxa Inadimplência | Qtd Empréstimos
- **Linha:** Valor concedido por AnoMes (fact_loan + Calendario)
- **Segmentadores:** Ano, status, faixa_valor

## Página 2 — Risco por Região

- **Barras:** Taxa inadimplência por district_name (dim_district)
- **Barras:** Valor total por região (ranking volume)
- **Tabela:** fact_agg_carteira com filtros cruzados

## Como gerar o .pbix

```powershell
# 1. Exportar dados (se ainda não feito)
python powerbi/export_views.py

# 2. Abrir Power BI Desktop → Obter dados → Texto/CSV → pasta powerbi/data/
# 3. Renomear tabelas conforme modelo acima
# 4. Criar relacionamentos e medidas (medidas.dax)
# 5. Salvar como powerbi/carteira_credito.pbix
```

Ou conectar via MySQL/MariaDB com cada arquivo `.sql` em Opções avançadas.

## Validação cruzada SQL ↔ PBI

| Métrica | SQL | PBI esperado |
|---|---|---|
| Taxa inadimplência | 11,14% | ~11,14% |
| Total empréstimos | 682 | 682 |
| Com cartão vs sem | 2,94% vs 13,87% | consistente |

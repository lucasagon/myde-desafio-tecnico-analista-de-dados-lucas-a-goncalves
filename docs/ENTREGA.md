# Checklist de entrega — validação final

**Participante:** Lucas Almeida Gonçalves  
**Data da validação:** 30/06/2026 (entrega final)  
**Repositório:** https://github.com/lucasagon/myde-desafio-tecnico-analista-de-dados-lucas-a-goncalves  
**Notion:** [MYDE — Desafio Técnico Analista de Dados](https://app.notion.com/p/38f5aecd550381b4a587caa909fc7445)

---

## Resultado automático (scripts) — 30/06/2026

| Verificação | Comando | Resultado |
|---|---|---|
| Views SQL + 9 consultas | `python python/validate_sql.py` | **OK** — 682 empréstimos, `fact_agg_carteira` 648 linhas |
| Pipeline Python | `python python/run_analysis.py` | **OK** — inadimplência **11,14%**, AUC **0,682** |
| Modelo PBI | `python powerbi/analyze_pbit.py` | **OK** — 9 tabelas, 12 medidas, calendário |
| Relatório PBI | `python powerbi/analyze_report.py` | **OK** — 3 páginas, slicers sincronizados loan+agg |

---

## Power BI — entrega final

| Item | Status |
|---|---|
| `.pbix` com dados (Import) | OK — ~21,7 MB |
| `.pbit` template | OK — ~2,5 MB |
| 3 páginas (Início, Visão Geral, Risco por Região) | OK |
| `fact_agg_carteira` com `status` (grain original) | OK |
| Slicers `fact_loan[status]` + `fact_agg_carteira[status]` sincronizados | OK |
| Assets `powerbi/bgs/` | OK |

---

## Entregáveis do PDF

| Requisito | Caminho | Status |
|---|---|---|
| Script `.sql` | `sql/consultas.sql` + `sql/views/` | OK |
| Power BI `.pbix` | `powerbi/desafio-analista-de-dados-myde-lucas-a-goncalves.pbix` | OK |
| Insights | `docs/INSIGHTS.md` | OK |
| Python (bônus) | `python/analise_risco.ipynb` | OK |
| Transparência IA | `docs/TRANSPARENCIA_IA.md` | OK |

---

## Documentação

| Documento | Conteúdo |
|---|---|
| `README.md` | Visão geral, setup, links Notion/Git |
| `docs/RUNBOOK.md` | Runbook de testes |
| `docs/TROUBLESHOOTING.md` | Problemas e soluções (ODBC, status, taxa) |
| `docs/SCHEMA.md` | Dicionário de dados |
| `docs/SQL.md` | Consultas + star schema |
| `docs/POWERBI.md` | ODBC, modelo, visuais, filtros |
| `docs/PYTHON.md` | Notebook + ML |
| `docs/INSIGHTS.md` | Achados para crédito |
| `docs/TRANSPARENCIA_IA.md` | Uso Cursor |

---

## Métricas de referência

| Métrica | Valor |
|---|---|
| Total empréstimos | 682 |
| Taxa inadimplência | 11,14% |
| Com cartão vs sem | 2,94% vs 13,87% |
| AUC (Python) | 0,682 |
| Moeda | CZK (Kč) |

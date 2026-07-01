# Runbook — testes e validação

**Participante:** Lucas Almeida Gonçalves  
**Repositório:** https://github.com/lucasagon/myde-desafio-tecnico-analista-de-dados-lucas-a-goncalves  
**Notion:** [MYDE — Desafio Técnico Analista de Dados](https://app.notion.com/p/38f5aecd550381b4a587caa909fc7445)

---

## Pré-requisitos

```bash
cp .env.example .env
pip install -r python/requirements.txt
```

---

## 1. SQL (obrigatório)

```powershell
cd D:\_Projects\myde
python python/validate_sql.py
```

**Esperado:**
- 9 views OK (dim: 77–5369 linhas; fact_loan: **682**; fact_trans: ~1M)
- `All SQL files validated.`

**Manual (opcional):** executar `sql/consultas.sql` no DBeaver e conferir query 3 → taxa **11,14%**.

---

## 2. Python — bônus (obrigatório na entrega)

```powershell
python python/run_analysis.py
```

**Esperado:**
- `Taxa inadimplencia: 11.14%`
- `AUC logistic regression: 0.682`

**Notebook:**
```powershell
cd python
jupyter notebook analise_risco.ipynb
```

---

## 3. Power BI — modelo (`.pbit`)

```powershell
python powerbi/analyze_pbit.py
python powerbi/validate_pbit.py
```

**Esperado:**
- 9 tabelas `dim_*` / `fact_*` + `dim_calendar` + `_medidas`
- 12 medidas DAX
- `fact_loan → dim_calendar` **ativo**
- `fact_trans → dim_calendar` **inativo**
- `fact_agg_carteira → dim_district` ativo

---

## 4. Power BI — relatório

```powershell
python powerbi/analyze_report.py
```

**Esperado:**
- **3 páginas:** Início, Visão Geral, Risco por Região
- KPIs: `Valor Total Emprestado`, `Taxa Inadimplência`, `Qtd Empréstimos`
- Slicers `fact_loan[status]` + `fact_agg_carteira[status]` (sincronizados)
- Tabela com `status` de `fact_agg_carteira`

---

## 5. Power BI — teste manual (avaliador)

| # | Teste | Resultado esperado |
|---|---|---|
| 1 | Abrir `.pbix` **offline** | Carrega sem reconectar ao MariaDB |
| 2 | KPI empréstimos | **682** |
| 3 | KPI taxa inadimplência (sem filtro status) | **~11,14%** |
| 4 | Moeda nos KPIs | **Kč** (CZK) |
| 5 | Slicer status = B | Filtra gráficos e tabela |
| 6 | Slicer Ano | Filtra linha temporal |
| 7 | Clique em barra de região | Filtros cruzados na tabela |
| 8 | Página Início | Logo + fundo |

---

## 6. Git — integridade da entrega

```powershell
git status
git log -1 --oneline
```

Confirmar que **não** há `.env` staged. Arquivos principais: `sql/`, `powerbi/*.pbix`, `powerbi/*.pbit`, `docs/`, `python/`.

---

## Métricas de referência

| Métrica | SQL | Python | PBI |
|---|---|---|---|
| Total empréstimos | 682 | 682 | 682 |
| Taxa inadimplência | 11,14% | 11,14% | ~11,14% |
| AUC (ML) | — | 0,682 | — |
| Moeda | CZK | CZK | Kč |

# Troubleshooting — problemas encontrados e soluções

**Notion:** [MYDE — Desafio Técnico Analista de Dados](https://app.notion.com/p/38f5aecd550381b4a587caa909fc7445)

---

## Power BI — conexão ODBC / MariaDB

| Erro | Causa | Solução |
|---|---|---|
| `Requested value 'None' was not found` | Connector MySQL nativo / .NET 32-bit | Usar **ODBC** com driver **MariaDB 3.2 (64-bit)** |
| `MariaDB ODBC 3.1 Driver` não encontrado | Versão do driver instalada ≠ referência na string | String: `DRIVER={MariaDB ODBC 3.2 Driver};...` |
| `uid can only be provided using credentials` | UID/PWD na string ODBC | Remover da string; credenciais na janela: `guest` / `ctu-relational` |
| Carga `fact_trans` muito lenta | ~1M linhas em Import | Aguardar ou montar rascunho sem `fact_trans`; fallback CSV |

**String ODBC:**
```
DRIVER={MariaDB ODBC 3.2 Driver};SERVER=relational.fel.cvut.cz;PORT=3306;DATABASE=financial
```

---

## Power BI — modelo e calendário

| Problema | Causa | Solução |
|---|---|---|
| Ambiguidade de caminhos de data | `dim_calendar` ativo em loan **e** trans | Manter **ativo** só em `fact_loan[loan_date]`; **inativo** em `fact_trans[trans_date]` |
| `LocalDateTable_*` no modelo | Auto-date do PBI | Ocultar na exibição; não usar nos visuais |
| Relações bidirecionais | Auto-detect do PBI | Preferir **single direction** (star schema); revisar `fact_loan ↔ dim_account` |

---

## Taxa de inadimplência — leitura dos números

| Sintoma | Explicação |
|---|---|
| Muitos **0%** e **100%** na tabela `fact_agg_carteira` | Grain inclui `status` (A/B/C/D): cada linha é um status → taxa 0% (A/C) ou 100% (B/D) **por linha** |
| Muitos distritos com **0%** no gráfico regional | Normal: 32 de 77 distritos não têm empréstimos B/D; amostra média ~9 empréstimos/distrito |
| KPI **100%** ou **0%** com slicer de status | Comportamento esperado: filtrar status=B → só maus → 100% |
| Taxa global correta | **11,14%** com slicer de status **sem seleção** (todos) |

**Decisão de modelagem:** mantido grain `distrito × mês × status × faixa` na agregada para filtros cruzados na tabela; taxa consolidada por região via medida DAX `Taxa Inadimplência Região` sobre `fact_loan`.

---

## Filtro de `status` não filtra gráfico / tabela

| Problema | Causa | Solução |
|---|---|---|
| Slicer `fact_loan[status]` não filtra a **tabela** | Não há relação direta `fact_loan` ↔ `fact_agg_carteira` | **Sincronizar slicers:** `fact_loan[status]` + `fact_agg_carteira[status]` (Exibir → Sincronizar slicers) |
| Gráfico não reage ao slicer | Editar interações desligada | Slicer → ícone de **filtro** no visual (não “nenhum”) |
| “Não há relacionamento” na tabela | Campo `status` de tabela errada ou coluna removida da query | Tabela: `fact_agg_carteira[status]`; gráficos/KPIs: `fact_loan[status]` |

---

## SQL

| Problema | Solução |
|---|---|
| Erro em `` `order` `` | Usar crases: `` SELECT * FROM `order` `` |
| View lenta no PBI | Modo **Import**; usar `fact_agg_carteira` para tabela analítica |

---

## Python

| Problema | Solução |
|---|---|
| Falha de conexão | Verificar `.env` (host, user, password) |
| `birth_number` vs `birth_date` | Versão hospedada CTU já traz `birth_date` decodificado |

---

## Scripts de diagnóstico no repo

```powershell
python powerbi/analyze_pbit.py      # tabelas, medidas, relações
python powerbi/analyze_report.py    # páginas e visuais
python powerbi/validate_pbit.py     # checklist de FKs
python python/validate_sql.py       # views + consultas
```

Ver também: [`docs/RUNBOOK.md`](RUNBOOK.md) | [`docs/POWERBI.md`](POWERBI.md)

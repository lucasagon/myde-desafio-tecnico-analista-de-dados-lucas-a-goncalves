# Desafio Técnico MYDE — Analista de Dados

**Participante:** Lucas Almeida Gonçalves — Nascimento: 27.06.1990.'

Take-home sobre o dataset **Berka/PKDD'99** (banco tcheco): SQL, Power BI, Python (bônus) e insights para a área de crédito.

## Documentação Notion

Hub do projeto: [MYDE — Desafio Técnico Analista de Dados](https://app.notion.com/p/38f5aecd550381b4a587caa909fc7445)

## Pré-requisitos

- Python 3.10+
- Power BI Desktop
- MariaDB Connector/ODBC **3.2 (64-bit)** para conexão no PBI
- DBeaver ou cliente MySQL (opcional)

## Setup rápido

```bash
git clone git@github.com:lucasagon/myde-desafio-tecnico-analista-de-dados-lucas-a-goncalves.git
cd myde-desafio-tecnico-analista-de-dados-lucas-a-goncalves
cp .env.example .env
pip install -r python/requirements.txt
```

## Estrutura do repositório

```
sql/                  # 9 consultas + views star schema (dim/ + fact/)
powerbi/              # .pbix, .pbit, medidas DAX, bgs/, scripts de validação
python/               # notebook de análise de risco + pipeline
docs/                 # documentação técnica, runbook, troubleshooting
reef/                 # PDF do desafio
```

## Como reproduzir

### SQL

```bash
python python/validate_sql.py
```

Executar `sql/consultas.sql` no DBeaver ou via cliente MySQL.

### Power BI

Conexão **ODBC ao MariaDB** (views em `sql/views/`, modo **Import**):

1. **Obter dados → ODBC** — `DRIVER={MariaDB ODBC 3.2 Driver};SERVER=relational.fel.cvut.cz;PORT=3306;DATABASE=financial`
2. Credenciais na janela do PBI: `guest` / `ctu-relational`
3. Para cada view, colar o SQL em **Instrução SQL**
4. Relacionamentos FK + `dim_calendar` + medidas em `_medidas` (`powerbi/medidas.dax`)
5. Relatório salvo: `powerbi/desafio-analista-de-dados-myde-lucas-a-goncalves.pbix` (3 páginas)

| Arquivo | Função |
|---|---|
| `desafio-analista-de-dados-myde-lucas-a-goncalves.pbix` | **Entrega** — relatório com dados |
| `desafio-analista-de-dados-myde-lucas-a-goncalves.pbit` | Template do modelo (sem dados) |

Assets visuais: `powerbi/bgs/`

**Validação:** [`docs/RUNBOOK.md`](docs/RUNBOOK.md) | **Problemas comuns:** [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md)

### Python

```bash
python python/run_analysis.py
cd python && jupyter notebook analise_risco.ipynb
```

## Dataset

- [Financial dataset (CTU)](https://relational.fel.cvut.cz/dataset/Financial)
- Host: `relational.fel.cvut.cz` | DB: `financial` | User: `guest`

## Entrega

**Git:** [github.com/lucasagon/myde-desafio-tecnico-analista-de-dados-lucas-a-goncalves](https://github.com/lucasagon/myde-desafio-tecnico-analista-de-dados-lucas-a-goncalves)

| Entregável | Caminho |
|---|---|
| SQL | `sql/consultas.sql` + `sql/views/` |
| Power BI | `powerbi/desafio-analista-de-dados-myde-lucas-a-goncalves.pbix` |
| Insights | `docs/INSIGHTS.md` |
| Python (bônus) | `python/analise_risco.ipynb` |
| Checklist final | `docs/ENTREGA.md` |

## Documentação

| Documento | Descrição |
|---|---|
| [Notion — Hub](https://app.notion.com/p/38f5aecd550381b4a587caa909fc7445) | Visão geral e subpáginas |
| [`docs/SCHEMA.md`](docs/SCHEMA.md) | Dicionário de dados |
| [`docs/SQL.md`](docs/SQL.md) | Consultas e star schema |
| [`docs/POWERBI.md`](docs/POWERBI.md) | Modelo, DAX, visuais |
| [`docs/PYTHON.md`](docs/PYTHON.md) | Notebook e ML |
| [`docs/INSIGHTS.md`](docs/INSIGHTS.md) | Achados para crédito |
| [`docs/RUNBOOK.md`](docs/RUNBOOK.md) | Runbook de testes |
| [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md) | ODBC, filtros, taxa |
| [`docs/TRANSPARENCIA_IA.md`](docs/TRANSPARENCIA_IA.md) | Uso de IA (Cursor) |
| [`docs/ENTREGA.md`](docs/ENTREGA.md) | Checklist de entrega |

## Transparência sobre uso de IA

Apoio ao desenvolvimento com **Cursor** (agente assistido). Detalhes: [`docs/TRANSPARENCIA_IA.md`](docs/TRANSPARENCIA_IA.md)

## Autor

**Lucas Almeida Gonçalves** (27.06.1990.')

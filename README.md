# Desafio Técnico MYDE — Analista de Dados

**Participante:** Lucas Almeida Gonçalves — Nascimento: 27/06/1990

Take-home sobre o dataset **Berka/PKDD'99** (banco tcheco): SQL, Power BI, Python (bônus) e insights para a área de crédito.

## Documentação Notion

Hub do projeto: [MYDE — Desafio Técnico Analista de Dados](https://app.notion.com/p/38f5aecd550381b4a587caa909fc7445)

## Pré-requisitos

- Python 3.10+
- Power BI Desktop
- DBeaver ou cliente MySQL (opcional)

## Setup rápido

```bash
git clone git@github.com:lucasagon/myde-desafio-tecnico-analista-de-dados-lucas-a-goncalves.git
cd myde-desafio-tecnico-analista-de-dados-lucas-a-goncalves
cp .env.example .env
# Edite .env com credenciais (valores públicos do dataset Berka no .env.example comentado)
pip install -r python/requirements.txt
```

## Estrutura do repositório

```
sql/                  # 9 consultas + views star schema (dim/ + fact/)
powerbi/              # medidas DAX, export CSV, guia do .pbix
python/               # notebook de análise de risco + config
docs/                 # SCHEMA, SQL, POWERBI, PYTHON, INSIGHTS, plans
reef/                 # PDF do desafio
```

## Como reproduzir

### SQL

```bash
python python/validate_sql.py
```

Executar `sql/consultas.sql` no DBeaver ou via cliente MySQL.

### Power BI

```bash
python powerbi/export_views.py
```

Seguir `powerbi/PBIX_BUILD.txt` e `docs/POWERBI.md`.

### Python

```bash
cd python && jupyter notebook analise_risco.ipynb
```

## Dataset

- [Financial dataset (CTU)](https://relational.fel.cvut.cz/dataset/Financial)
- Host: `relational.fel.cvut.cz` | DB: `financial` | User: `guest`

## Autor

**Lucas Almeida Gonçalves** (27/06/1990)  
Repositório: https://github.com/lucasagon/myde-desafio-tecnico-analista-de-dados-lucas-a-goncalves

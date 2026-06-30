# Parte 3 — Python

Arquivo: `python/analise_risco.ipynb`

## Dependências

```bash
pip install -r python/requirements.txt
cp .env.example .env   # preencher credenciais
```

## Etapas implementadas

| Etapa | Conteúdo |
|---|---|
| 1. Leitura | Tabelas via SQLAlchemy + `.env` |
| 2. EDA | Missing values, describe, distribuição de status |
| 3. Risco | Perfil bons (A/C) vs maus (B/D) por idade, valor, distrito |
| 4. Plotly | Histograma idade, boxplot valor, barras por faixa, scatter salário×inadimplência |
| 5. ML | Regressão logística, matriz de confusão, AUC |

## Resultados validados (`python/run_analysis.py`)

| Métrica | Valor |
|---|---|
| Taxa inadimplência (baseline) | 11,14% |
| AUC (logistic regression) | 0,682 |
| Features | idade, amount, duration, avg_salary, unemployment_1995 |

## Reprodução

```bash
cd python
jupyter notebook analise_risco.ipynb
```

Ou validação rápida: `python run_analysis.py`

## Limitações do modelo

- Dataset pequeno (682 empréstimos), classes desbalanceadas
- Sem validação temporal (risco de leakage)
- Variáveis macro do distrito são proxy agregado

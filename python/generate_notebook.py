#!/usr/bin/env python3
"""Generate analise_risco.ipynb programmatically."""
import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []

cells.append(nbf.v4.new_markdown_cell("""# Análise de Risco — Desafio MYDE Analista de Dados

Dataset Berka/PKDD'99 (banco `financial`).  
Bons pagadores: status A/C | Maus: B/D"""))

cells.append(nbf.v4.new_code_cell("""import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.io as pio
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, RocCurveDisplay
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

from config import DATABASE_URL

pio.renderers.default = 'notebook'
engine = create_engine(DATABASE_URL)
print('Conectado:', DATABASE_URL.split('@')[1])"""))

cells.append(nbf.v4.new_markdown_cell("## 1. Leitura e tratamento"))

cells.append(nbf.v4.new_code_cell("""TABLES = ['client', 'account', 'disp', 'district', 'loan', 'card']
dfs = {t: pd.read_sql(f'SELECT * FROM `{t}`' if t == 'order' else f'SELECT * FROM {t}', engine) for t in TABLES}

client = dfs['client']
account = dfs['account']
district = dfs['district']
loan = dfs['loan']
disp = dfs['disp']
card = dfs['card']

client['birth_date'] = pd.to_datetime(client['birth_date'])
client['idade'] = ((pd.Timestamp('1998-12-31') - client['birth_date']).dt.days / 365.25).astype(int)
loan['date'] = pd.to_datetime(loan['date'])
loan['status_grupo'] = np.where(loan['status'].isin(['A','C']), 'bom', 'mau')
loan['faixa_valor'] = pd.cut(loan['amount'], bins=[0, 50000, 150000, np.inf], labels=['Pequeno','Médio','Grande'])

district = district.rename(columns={'A2':'district_name','A11':'avg_salary','A12':'unemployment_1995'})

loan_enriched = loan.merge(account[['account_id','district_id']], on='account_id')
loan_enriched = loan_enriched.merge(district[['district_id','district_name','avg_salary','unemployment_1995']], on='district_id')
owner = disp[disp['type']=='OWNER'][['account_id','client_id']]
loan_enriched = loan_enriched.merge(owner, on='account_id', how='left')
loan_enriched = loan_enriched.merge(client[['client_id','gender','idade']], on='client_id', how='left')

print('Empréstimos:', len(loan_enriched))
loan_enriched.head()"""))

cells.append(nbf.v4.new_markdown_cell("## 2. EDA"))

cells.append(nbf.v4.new_code_cell("""print('Missing loan:', loan_enriched.isnull().sum().sort_values(ascending=False).head())
print(loan_enriched.describe(include='all'))
print('\\nStatus:', loan_enriched['status'].value_counts())
print('Taxa inadimplência:', (loan_enriched['status_grupo']=='mau').mean()*100, '%')"""))

cells.append(nbf.v4.new_markdown_cell("## 3. Análise de risco — bons vs maus"))

cells.append(nbf.v4.new_code_cell("""compare_cols = ['idade','amount','duration','avg_salary','unemployment_1995']
profile = loan_enriched.groupby('status_grupo')[compare_cols].agg(['mean','median','std']).round(2)
profile"""))

cells.append(nbf.v4.new_markdown_cell("## 4. Visualizações Plotly"))

cells.append(nbf.v4.new_code_cell("""fig1 = px.histogram(loan_enriched, x='idade', color='status_grupo', barmode='overlay',
                      opacity=0.7, title='Distribuição de idade: bons vs maus pagadores')
fig1.show()

fig2 = px.box(loan_enriched, x='status_grupo', y='amount', color='status_grupo',
              title='Valor do empréstimo: bons vs maus pagadores')
fig2.show()

inad_faixa = loan_enriched.groupby('faixa_valor', observed=True).apply(
    lambda x: (x['status_grupo']=='mau').mean()*100, include_groups=False
).reset_index(name='taxa_inadimplencia_pct')
fig3 = px.bar(inad_faixa, x='faixa_valor', y='taxa_inadimplencia_pct',
              title='Taxa de inadimplência por faixa de valor')
fig3.show()

reg_inad = loan_enriched.groupby('district_id').agg(
    taxa_inad=('status_grupo', lambda s: (s=='mau').mean()*100),
    avg_salary=('avg_salary','first')
).reset_index()
fig4 = px.scatter(reg_inad, x='avg_salary', y='taxa_inad',
                  title='Salario medio do distrito vs taxa de inadimplencia')
fig4.show()"""))

cells.append(nbf.v4.new_markdown_cell("## 5. Modelagem ML — Regressão logística"))

cells.append(nbf.v4.new_code_cell("""features = ['idade','amount','duration','avg_salary','unemployment_1995']
df_ml = loan_enriched.dropna(subset=features).copy()
df_ml['target'] = (df_ml['status_grupo'] == 'mau').astype(int)

X = df_ml[features]
y = df_ml['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)

model = LogisticRegression(max_iter=1000, class_weight='balanced')
model.fit(X_train_s, y_train)
y_pred = model.predict(X_test_s)
y_prob = model.predict_proba(X_test_s)[:,1]

print(classification_report(y_test, y_pred))
print('AUC:', round(roc_auc_score(y_test, y_prob), 3))
print('Matriz de confusão:\\n', confusion_matrix(y_test, y_pred))

RocCurveDisplay.from_predictions(y_test, y_prob)
plt.title('Curva ROC — previsão de inadimplência')
plt.show()

# Limitações: dataset pequeno (682), desbalanceado, sem validação temporal"""))

nb['cells'] = cells
path = __file__.replace('generate_notebook.py', 'analise_risco.ipynb')
with open(path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)
print('Written', path)

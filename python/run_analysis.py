"""Run full analysis pipeline (notebook logic) for validation and INSIGHTS."""
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, confusion_matrix
from sklearn.preprocessing import StandardScaler

from config import DATABASE_URL

engine = create_engine(DATABASE_URL)
client = pd.read_sql("SELECT * FROM client", engine)
account = pd.read_sql("SELECT * FROM account", engine)
district = pd.read_sql("SELECT * FROM district", engine)
loan = pd.read_sql("SELECT * FROM loan", engine)
disp = pd.read_sql("SELECT * FROM disp", engine)

client["birth_date"] = pd.to_datetime(client["birth_date"])
client["idade"] = ((pd.Timestamp("1998-12-31") - client["birth_date"]).dt.days / 365.25).astype(int)
loan["status_grupo"] = np.where(loan["status"].isin(["A", "C"]), "bom", "mau")
loan["faixa_valor"] = pd.cut(
    loan["amount"], bins=[0, 50000, 150000, np.inf], labels=["Pequeno", "Médio", "Grande"]
)

district = district.rename(columns={"A2": "district_name", "A11": "avg_salary", "A12": "unemployment_1995"})
loan_enriched = loan.merge(account[["account_id", "district_id"]], on="account_id")
loan_enriched = loan_enriched.merge(
    district[["district_id", "district_name", "avg_salary", "unemployment_1995"]], on="district_id"
)
owner = disp[disp["type"] == "OWNER"][["account_id", "client_id"]]
loan_enriched = loan_enriched.merge(owner, on="account_id", how="left")
loan_enriched = loan_enriched.merge(client[["client_id", "gender", "idade"]], on="client_id", how="left")

taxa = (loan_enriched["status_grupo"] == "mau").mean() * 100
print(f"Taxa inadimplencia: {taxa:.2f}%")

features = ["idade", "amount", "duration", "avg_salary", "unemployment_1995"]
df_ml = loan_enriched.dropna(subset=features).copy()
df_ml["target"] = (df_ml["status_grupo"] == "mau").astype(int)
X_train, X_test, y_train, y_test = train_test_split(
    df_ml[features], df_ml["target"], test_size=0.25, random_state=42, stratify=df_ml["target"]
)
scaler = StandardScaler()
model = LogisticRegression(max_iter=1000, class_weight="balanced")
model.fit(scaler.fit_transform(X_train), y_train)
y_prob = model.predict_proba(scaler.transform(X_test))[:, 1]
auc = roc_auc_score(y_test, y_prob)
print(f"AUC logistic regression: {auc:.3f}")
print("Confusion matrix:\n", confusion_matrix(y_test, model.predict(scaler.transform(X_test))))

"""Export star schema views to CSV — FALLBACK only (offline / slow MariaDB).

Primary path for Power BI: ODBC (MariaDB 3.2) with SQL from sql/views/*.sql — see docs/POWERBI.md
See docs/POWERBI.md
"""
import os
import glob
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

url = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
engine = create_engine(url)
out_dir = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(out_dir, exist_ok=True)

base = os.path.join(os.path.dirname(__file__), "..", "sql", "views")
for folder in ("dim", "fact"):
    for path in sorted(glob.glob(os.path.join(base, folder, "*.sql"))):
        name = os.path.splitext(os.path.basename(path))[0]
        with open(path, encoding="utf-8") as f:
            sql = f.read()
        print(f"Exporting {name}...")
        df = pd.read_sql(sql.replace("%", "%%"), engine)
        csv_path = os.path.join(out_dir, f"{name}.csv")
        df.to_csv(csv_path, index=False)
        print(f"  -> {csv_path} ({len(df)} rows)")

print("Done.")

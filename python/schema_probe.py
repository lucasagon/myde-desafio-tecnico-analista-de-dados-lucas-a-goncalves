"""Schema discovery script for financial database."""
import os
import json
import pymysql
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

conn = pymysql.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", 3306)),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    connect_timeout=30,
)
cur = conn.cursor()

tables = []
cur.execute("SHOW TABLES")
for (tname,) in cur.fetchall():
    cur.execute(f"DESCRIBE `{tname}`")
    cols = [
        {"field": c[0], "type": c[1], "null": c[2], "key": c[3], "default": str(c[4]), "extra": c[5]}
        for c in cur.fetchall()
    ]
    cur.execute(f"SELECT COUNT(*) FROM `{tname}`")
    count = cur.fetchone()[0]
    cur.execute(f"SELECT * FROM `{tname}` LIMIT 2")
    sample = cur.fetchall()
    tables.append({"name": tname, "rows": count, "columns": cols, "sample_rows": len(sample)})

# Cardinalities
stats = {}
cur.execute("SELECT status, COUNT(*) FROM loan GROUP BY status ORDER BY status")
stats["loan_status"] = cur.fetchall()
cur.execute("SELECT type, COUNT(*) FROM disp GROUP BY type")
stats["disp_type"] = cur.fetchall()
cur.execute("SELECT type, COUNT(*) FROM card GROUP BY type")
stats["card_type"] = cur.fetchall()
cur.execute("SELECT MIN(`date`), MAX(`date`) FROM loan")
stats["loan_date_range"] = cur.fetchone()
cur.execute("SELECT MIN(`date`), MAX(`date`) FROM trans")
stats["trans_date_range"] = cur.fetchone()
cur.execute("SELECT MIN(birth_date), MAX(birth_date) FROM client")
stats["birth_date_range"] = cur.fetchone()

out = {"tables": tables, "stats": stats}
print(json.dumps(out, indent=2, default=str))
conn.close()

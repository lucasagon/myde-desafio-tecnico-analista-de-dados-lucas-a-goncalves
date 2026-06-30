"""Validate SQL queries and views against MariaDB."""
import os
import glob
import pymysql
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

conn = pymysql.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", 3306)),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    connect_timeout=60,
)
cur = conn.cursor()

base = os.path.join(os.path.dirname(__file__), "..", "sql")
files = [os.path.join(base, "consultas.sql")]
files += sorted(glob.glob(os.path.join(base, "views", "dim", "*.sql")))
files += sorted(glob.glob(os.path.join(base, "views", "fact", "*.sql")))

errors = []
for path in files:
    name = os.path.relpath(path, base)
    with open(path, encoding="utf-8") as f:
        sql = f.read().strip().rstrip(";")
    # consultas.sql has multiple statements — validate each CTE block separately
    if name == "consultas.sql":
        parts = [p.strip() for p in sql.split(";") if p.strip() and not p.strip().startswith("--")]
        for i, part in enumerate(parts, 1):
            try:
                cur.execute(part)
                rows = cur.fetchall()
                print(f"OK consultas.sql#{i}: {len(rows)} rows")
            except Exception as e:
                errors.append((f"consultas.sql#{i}", str(e)))
                print(f"FAIL consultas.sql#{i}: {e}")
    else:
        try:
            cur.execute(f"SELECT COUNT(*) FROM ({sql}) AS q")
            count = cur.fetchone()[0]
            print(f"OK {name}: {count} rows")
        except Exception as e:
            errors.append((name, str(e)))
            print(f"FAIL {name}: {e}")

conn.close()
if errors:
    raise SystemExit(f"{len(errors)} validation error(s)")
print("All SQL files validated.")

"""Run consultas.sql queries and print key metrics."""
import os
import re
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
path = os.path.join(os.path.dirname(__file__), "..", "sql", "consultas.sql")
text = open(path, encoding="utf-8").read()
queries = [q.strip() for q in text.split(";") if q.strip() and "SELECT" in q.upper()]
for i, q in enumerate(queries, 1):
    cur.execute(q)
    rows = cur.fetchall()
    print(f"Query {i}: {len(rows)} rows | sample: {rows[:2]}")
conn.close()

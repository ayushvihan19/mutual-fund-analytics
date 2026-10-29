
import sqlite3
from pathlib import Path

db_path = Path("data/processed/mutual_fund_analytics.db")
sql_path = Path("sql/queries.sql")

# Read SQL and remove comment lines
sql_text = "\n".join(
    line for line in sql_path.read_text(encoding="utf-8").splitlines()
    if not line.strip().startswith("--")
)

queries = [q.strip() for q in sql_text.split(";") if q.strip()]

with sqlite3.connect(db_path) as conn:
    print(f"Total queries found: {len(queries)}")

    passed = 0
    for i, query in enumerate(queries, start=1):
        try:
            result = conn.execute(query)
            rows = result.fetchall()
            print(f"Query {i}: PASS ({len(rows)} result rows)")
            passed += 1
        except Exception as error:
            print(f"Query {i}: FAIL - {error}")

    print(f"\nSummary: {passed}/{len(queries)} queries passed.")

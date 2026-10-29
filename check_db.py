
import sqlite3

db = "data/processed/mutual_fund_analytics.db"

with sqlite3.connect(db) as conn:
    tables = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    ).fetchall()

    for (table,) in tables:
        print(f"\n--- {table} ---")
        for col in conn.execute(f'PRAGMA table_info("{table}")'):
            print(col[1], "|", col[2], "| primary key:", col[5])

    print("\nForeign key issues:")
    print(conn.execute("PRAGMA foreign_key_check").fetchall())

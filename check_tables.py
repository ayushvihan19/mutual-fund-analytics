import sqlite3
from pathlib import Path

db = Path("data/processed/mutual_fund_analytics.db")

if not db.exists():
    print("Database file nahi mili:", db.resolve())
else:
    conn = sqlite3.connect(str(db))
    tables = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    ).fetchall()

    print("Existing database tables:")
    for table in tables:
        print("-", table[0])

    conn.close()
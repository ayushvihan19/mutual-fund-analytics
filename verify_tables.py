
import sqlite3

db_path = r"data/processed/bluestock_mf.db"

conn = sqlite3.connect(db_path)

print("Database tables:")
for row in conn.execute(
    "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"
):
    print("-", row[0])

conn.close()

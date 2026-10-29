
import sqlite3

db_path = "data/processed/bluestock_mf.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
      AND name NOT LIKE 'sqlite_%'
    ORDER BY name
""")

tables = cur.fetchall()

print("DATABASE TABLES AND ROW COUNTS")
print("-" * 40)

for (table_name,) in tables:
    cur.execute(f'SELECT COUNT(*) FROM "{table_name}"')
    count = cur.fetchone()[0]
    print(f"{table_name}: {count} rows")

print("-" * 40)
print("Total tables:", len(tables))

conn.close()

import sqlite3

db_path = "data/processed/bluestock_mf.db"

conn = sqlite3.connect(db_path)
conn.execute("PRAGMA foreign_keys = ON")

print("Foreign key errors:", conn.execute(
    "PRAGMA foreign_key_check"
).fetchall())

print("\nDatabase tables:")
tables = conn.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
    ORDER BY name
""").fetchall()

for table in tables:
    name = table[0]
    count = conn.execute(
        f"SELECT COUNT(*) FROM [{name}]"
    ).fetchone()[0]
    print(f"{name}: {count} rows")

conn.close()
print("\nVerification completed!")
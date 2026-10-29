
import sqlite3

db = "data/processed/mutual_fund_analytics.db"
conn = sqlite3.connect(db)

checks = [
    ("Fund master codes", """
        SELECT COUNT(DISTINCT amfi_code) FROM fund_master
    """),
    ("NAV history rows", """
        SELECT COUNT(*) FROM nav_history
    """),
    ("NAV codes missing from fund master", """
        SELECT COUNT(DISTINCT n.amfi_code)
        FROM nav_history n
        LEFT JOIN fund_master f ON n.amfi_code = f.amfi_code
        WHERE f.amfi_code IS NULL
    """),
    ("Transaction rows", """
        SELECT COUNT(*) FROM investor_transactions
    """),
    ("Transaction codes missing from fund master", """
        SELECT COUNT(DISTINCT t.amfi_code)
        FROM investor_transactions t
        LEFT JOIN fund_master f ON t.amfi_code = f.amfi_code
        WHERE f.amfi_code IS NULL
    """),
    ("NAV dates", """
        SELECT COUNT(DISTINCT date) FROM nav_history
    """),
    ("Transaction dates", """
        SELECT COUNT(DISTINCT transaction_date)
        FROM investor_transactions
    """)
]

for label, query in checks:
    result = conn.execute(query).fetchone()[0]
    print(f"{label}: {result}")
print("Fund master duplicate codes:",
      conn.execute("""
          SELECT COUNT(*) FROM (
              SELECT amfi_code
              FROM fund_master
              GROUP BY amfi_code
              HAVING COUNT(*) > 1
          )
      """).fetchone()[0])

print("Duplicate NAV scheme/date pairs:",
      conn.execute("""
          SELECT COUNT(*) FROM (
              SELECT amfi_code, date
              FROM nav_history
              GROUP BY amfi_code, date
              HAVING COUNT(*) > 1
          )
      """).fetchone()[0])

print("Duplicate transaction source rows:",
      conn.execute("""
          SELECT COUNT(*) FROM (
              SELECT investor_id, transaction_date, amfi_code,
                     transaction_type, amount_inr
              FROM investor_transactions
              GROUP BY investor_id, transaction_date, amfi_code,
                       transaction_type, amount_inr
              HAVING COUNT(*) > 1
          )
      """).fetchone()[0])
conn.close()

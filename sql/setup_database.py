

from pathlib import Path
import sqlite3
import pandas as pd

# Project folders
PROJECT_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_DIR / "data" / "raw"
DB_PATH = PROJECT_DIR / "data" / "processed" / "mutual_fund_analytics.db"
SQL_PATH = PROJECT_DIR / "sql" / "mutual_fund_analysis.sql"

# CSV filename patterns and corresponding database tables
FILES = {
    "investor_transactions": "*investor_transactions*.csv",
    "portfolio_holdings": "*portfolio_holdings.csv",
    "benchmark_indices": "*benchmark_indices.csv",
    "fund_master": "*fund_master.csv",
    "nav_history": "*nav_history.csv",
    "aum_by_fund_house": "*aum_by_fund_house.csv",
    "monthly_sip_inflows": "*monthly_sip_inflows.csv",
    "category_inflows": "*category_inflows.csv",
    "industry_folio_count": "*industry_folio_count.csv",
    "scheme_performance": "*scheme_performance.csv",
}

DB_PATH.parent.mkdir(parents=True, exist_ok=True)

with sqlite3.connect(DB_PATH) as conn:
    for table, pattern in FILES.items():
        matches = list(RAW_DIR.glob(pattern))

        if not matches:
            print(f"SKIPPED: No CSV found for {table}")
            continue

        # Use the first matching source CSV
        csv_path = matches[0]
        df = pd.read_csv(csv_path)

        df.to_sql(table, conn, if_exists="replace", index=False)
        print(f"LOADED: {table} — {len(df)} rows")

    print("\n--- TESTING SQL QUERIES ---")

    sql_text = SQL_PATH.read_text(encoding="utf-8")
    queries = [
        q.strip()
        for q in sql_text.split(";")
        if q.strip() and not q.strip().startswith("--")
    ]

    for i, query in enumerate(queries, start=1):
        try:
            result = pd.read_sql_query(query, conn)
            print(f"\nQuery {i}: SUCCESS ({len(result)} rows)")
            print(result.head(5).to_string(index=False))
        except Exception as error:
            print(f"\nQuery {i}: FAILED")
            print(error)

print(f"\nDatabase saved at: {DB_PATH}")

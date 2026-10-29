from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parent
SOURCE_DB = ROOT / "data" / "processed" / "mutual_fund_analytics.db"
TARGET_DB = ROOT / "data" / "processed" / "bluestock_mf.db"
TEMP_DB = ROOT / "data" / "processed" / "bluestock_mf_building.db"
SCHEMA_FILE = ROOT / "sql" / "schema.sql"


def clean_date(value):
    parsed = pd.to_datetime(value, errors="coerce")
    if pd.isna(parsed):
        return None
    return parsed.strftime("%Y-%m-%d")


def main():
    if not SOURCE_DB.exists():
        raise FileNotFoundError(f"Source database not found: {SOURCE_DB}")

    if not SCHEMA_FILE.exists():
        raise FileNotFoundError(f"Schema file not found: {SCHEMA_FILE}")

    if TARGET_DB.exists():
        raise FileExistsError(
            f"{TARGET_DB} already exists. Existing database was not changed."
        )

    if TEMP_DB.exists():
        TEMP_DB.unlink()

    source = sqlite3.connect(SOURCE_DB)
    target = sqlite3.connect(TEMP_DB)

    try:
        target.execute("PRAGMA foreign_keys = ON")

        funds = pd.read_sql_query("SELECT * FROM fund_master", source)
        nav = pd.read_sql_query("SELECT * FROM nav_history", source)
        transactions = pd.read_sql_query(
            "SELECT * FROM investor_transactions", source
        )
        performance = pd.read_sql_query(
            "SELECT * FROM scheme_performance", source
        )
        aum = pd.read_sql_query(
            "SELECT * FROM aum_by_fund_house", source
        )

        # Normalize dates and validate required values.
        nav["date_key"] = nav["date"].map(clean_date)
        transactions["date_key"] = transactions["transaction_date"].map(clean_date)
        aum["date_key"] = aum["date"].map(clean_date)

        if nav["date_key"].isna().any():
            raise ValueError("Some NAV dates could not be parsed.")
        if transactions["date_key"].isna().any():
            raise ValueError("Some transaction dates could not be parsed.")
        if aum["date_key"].isna().any():
            raise ValueError("Some AUM dates could not be parsed.")

        if funds["amfi_code"].duplicated().any():
            raise ValueError("Duplicate AMFI codes found in fund_master.")
        if nav.duplicated(["amfi_code", "date_key"]).any():
            raise ValueError("Duplicate fund/date pairs found in NAV data.")
        if performance["amfi_code"].duplicated().any():
            raise ValueError("Duplicate AMFI codes found in performance data.")
        if aum.duplicated(["date_key", "fund_house"]).any():
            raise ValueError("Duplicate date/fund-house pairs found in AUM data.")

        fund_codes = set(funds["amfi_code"].dropna())
        for label, frame in [
            ("NAV", nav),
            ("transactions", transactions),
            ("performance", performance),
        ]:
            unknown = set(frame["amfi_code"].dropna()) - fund_codes
            if unknown:
                raise ValueError(f"{label} contains unknown AMFI codes: {list(unknown)[:5]}")

        all_dates = sorted(
            set(nav["date_key"])
            | set(transactions["date_key"])
            | set(aum["date_key"])
        )

        houses = sorted(
            set(funds["fund_house"].dropna().astype(str).str.strip())
            | set(aum["fund_house"].dropna().astype(str).str.strip())
        )
        houses = [house for house in houses if house]

        # Create star schema with keys and foreign-key constraints.
        target.executescript("""
        CREATE TABLE dim_fund (
            amfi_code INTEGER PRIMARY KEY,
            scheme_name TEXT NOT NULL,
            fund_house TEXT,
            category TEXT,
            sub_category TEXT,
            plan TEXT,
            expense_ratio_pct REAL,
            risk_category TEXT
        );

        CREATE TABLE dim_date (
            date_key TEXT PRIMARY KEY,
            year INTEGER NOT NULL,
            month INTEGER NOT NULL,
            day INTEGER NOT NULL
        );

        CREATE TABLE dim_fund_house (
            fund_house_id INTEGER PRIMARY KEY,
            fund_house TEXT UNIQUE NOT NULL
        );

        CREATE TABLE fact_nav (
            amfi_code INTEGER NOT NULL,
            date_key TEXT NOT NULL,
            nav REAL,
            PRIMARY KEY (amfi_code, date_key),
            FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
            FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
        );

        CREATE TABLE fact_transactions (
            transaction_id INTEGER PRIMARY KEY,
            investor_id TEXT,
            amfi_code INTEGER NOT NULL,
            date_key TEXT NOT NULL,
            transaction_type TEXT,
            amount_inr REAL,
            state TEXT,
            city TEXT,
            city_tier TEXT,
            age_group TEXT,
            gender TEXT,
            annual_income_lakh REAL,
            payment_mode TEXT,
            kyc_status TEXT,
            FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
            FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
        );

        CREATE TABLE fact_performance (
            amfi_code INTEGER PRIMARY KEY,
            return_1yr_pct REAL,
            return_3yr_pct REAL,
            return_5yr_pct REAL,
            benchmark_3yr_pct REAL,
            alpha REAL,
            beta REAL,
            sharpe_ratio REAL,
            sortino_ratio REAL,
            std_dev_ann_pct REAL,
            max_drawdown_pct REAL,
            aum_crore REAL,
            expense_ratio_pct REAL,
            morningstar_rating REAL,
            risk_grade TEXT,
            FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
        );

        CREATE TABLE fact_aum (
            date_key TEXT NOT NULL,
            fund_house_id INTEGER NOT NULL,
            aum_lakh_crore REAL,
            aum_crore REAL,
            num_schemes INTEGER,
            PRIMARY KEY (date_key, fund_house_id),
            FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
            FOREIGN KEY (fund_house_id) REFERENCES dim_fund_house(fund_house_id)
        );
        """)

        # Populate dimensions.
        fund_cols = [
            "amfi_code", "scheme_name", "fund_house", "category",
            "sub_category", "plan", "expense_ratio_pct", "risk_category"
        ]
        funds[fund_cols].to_sql("dim_fund", target, if_exists="append", index=False)

        date_rows = []
        for date_value in all_dates:
            date_obj = pd.Timestamp(date_value)
            date_rows.append((
                date_value, int(date_obj.year),
                int(date_obj.month), int(date_obj.day)
            ))
        target.executemany(
            "INSERT INTO dim_date VALUES (?, ?, ?, ?)", date_rows
        )

        house_ids = {name: i for i, name in enumerate(houses, start=1)}
        target.executemany(
            "INSERT INTO dim_fund_house VALUES (?, ?)",
            [(house_ids[name], name) for name in houses]
        )

        # Populate fact tables.
        nav_rows = [
            (int(row.amfi_code), row.date_key, row.nav)
            for row in nav.itertuples(index=False)
        ]
        target.executemany(
            "INSERT INTO fact_nav (amfi_code, date_key, nav) VALUES (?, ?, ?)",
            nav_rows
        )

        transaction_rows = []
        for i, row in enumerate(transactions.itertuples(index=False), start=1):
            transaction_rows.append((
                i, row.investor_id, int(row.amfi_code), row.date_key,
                row.transaction_type, row.amount_inr, row.state, row.city,
                row.city_tier, row.age_group, row.gender,
                row.annual_income_lakh, row.payment_mode, row.kyc_status
            ))
        target.executemany("""
            INSERT INTO fact_transactions (
                transaction_id, investor_id, amfi_code, date_key,
                transaction_type, amount_inr, state, city, city_tier,
                age_group, gender, annual_income_lakh, payment_mode, kyc_status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, transaction_rows)

        performance_cols = [
            "amfi_code", "return_1yr_pct", "return_3yr_pct",
            "return_5yr_pct", "benchmark_3yr_pct", "alpha", "beta",
            "sharpe_ratio", "sortino_ratio", "std_dev_ann_pct",
            "max_drawdown_pct", "aum_crore", "expense_ratio_pct",
            "morningstar_rating", "risk_grade"
        ]
        performance[performance_cols].to_sql(
            "fact_performance", target, if_exists="append", index=False
        )

        aum_rows = []
        for row in aum.itertuples(index=False):
            house = str(row.fund_house).strip()
            if not house or house not in house_ids:
                raise ValueError(f"Missing fund-house dimension value: {house!r}")
            aum_rows.append((
                row.date_key, house_ids[house], row.aum_lakh_crore,
                row.aum_crore, row.num_schemes
            ))
        target.executemany(
            "INSERT INTO fact_aum VALUES (?, ?, ?, ?, ?)", aum_rows
        )

        target.commit()

        # Final validation.
        violations = target.execute("PRAGMA foreign_key_check").fetchall()
        if violations:
            raise ValueError(f"Foreign-key validation failed: {violations[:5]}")

        print("\nDATABASE CREATED AND VALIDATED")
        for table in [
            "dim_fund", "dim_date", "dim_fund_house",
            "fact_nav", "fact_transactions", "fact_performance", "fact_aum"
        ]:
            count = target.execute(
                f"SELECT COUNT(*) FROM {table}"
            ).fetchone()[0]
            print(f"{table}: {count:,} rows")

        target.close()
        source.close()

        TEMP_DB.replace(TARGET_DB)

        print(f"\nSaved database: {TARGET_DB}")
        print("Foreign-key check: PASSED")

    except Exception:
        target.close()
        source.close()
        if TEMP_DB.exists():
            TEMP_DB.unlink()
        raise


if __name__ == "__main__":
    main()
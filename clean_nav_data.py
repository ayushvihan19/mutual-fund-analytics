
from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

TODAY = pd.Timestamp.today().normalize()

for file_path in sorted(RAW_DIR.glob("*_nav.csv")):
    df = pd.read_csv(file_path)

    df["date"] = pd.to_datetime(
        df["date"], format="mixed", dayfirst=True, errors="coerce"
    )
    df["nav"] = pd.to_numeric(df["nav"], errors="coerce")

    invalid_dates = df["date"].isna().sum()
    invalid_navs = df["nav"].isna().sum()
    nonpositive_navs = (df["nav"] <= 0).sum()
    future_dates = (df["date"] > TODAY).sum()
    duplicate_rows = df.duplicated().sum()
    duplicate_dates = df["date"].duplicated().sum()

    print(f"\nFile: {file_path.name}")
    print("Invalid dates:", invalid_dates)
    print("Invalid NAV values:", invalid_navs)
    print("Non-positive NAVs:", nonpositive_navs)
    print("Future-dated rows:", future_dates)
    print("Duplicate rows:", duplicate_rows)
    print("Duplicate dates:", duplicate_dates)

    # Remove only exact duplicate rows.
    df = df.drop_duplicates()

    # Sort dates chronologically.
    df = df.sort_values("date")

    # Keep questionable records for review instead of silently deleting them.
    output_path = PROCESSED_DIR / file_path.name
    df.to_csv(output_path, index=False, date_format="%Y-%m-%d")
    print("Saved:", output_path)

print("\nCleaning and validation pass complete.")


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

    original_rows = len(df)

    # Remove invalid dates and invalid or non-positive NAV values.
    df = df.dropna(subset=["date", "nav"])
    df = df[df["nav"] > 0]

    # Exclude dates later than today.
    df = df[df["date"] <= TODAY]

    # Remove duplicate rows and sort chronologically.
    df = df.drop_duplicates()
    df = df.sort_values("date")

    # Keep one record per date, retaining the last row after sorting.
    df = df.drop_duplicates(subset=["date"], keep="last")

    output_path = PROCESSED_DIR / file_path.name
    df.to_csv(output_path, index=False, date_format="%Y-%m-%d")

    print(f"\nFile: {file_path.name}")
    print("Original rows:", original_rows)
    print("Processed rows:", len(df))
    print("Rows removed:", original_rows - len(df))
    print("Dates sorted:", df["date"].is_monotonic_increasing)
    print("Remaining invalid NAVs:", (df["nav"] <= 0).sum())
    print("Remaining future dates:", (df["date"] > TODAY).sum())
    print("Saved:", output_path)

print("\nCleaning complete.")

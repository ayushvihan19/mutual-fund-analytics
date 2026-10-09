
from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw")

for file_path in sorted(RAW_DIR.glob("*_nav.csv")):
    print("\n" + "=" * 55)
    print("File:", file_path.name)

    df = pd.read_csv(file_path)

    # Parse both YYYY-MM-DD and DD-MM-YYYY formats
    dates = pd.to_datetime(df["date"], format="mixed", dayfirst=True,
                           errors="coerce")
    nav = pd.to_numeric(df["nav"], errors="coerce")

    print("Rows:", len(df))
    print("Invalid dates:", dates.isna().sum())
    print("Invalid NAV values:", nav.isna().sum())
    print("Non-positive NAV values:", (nav <= 0).sum())
    print("Duplicate dates:", dates.duplicated().sum())
    print("Date range:", dates.min(), "to", dates.max())
    print("Already sorted:", dates.is_monotonic_increasing)

print("\nDate validation complete.")
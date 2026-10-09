
from pathlib import Path
import pandas as pd

PROCESSED_DIR = Path("data/processed")
TODAY = pd.Timestamp.today().normalize()

for file_path in sorted(PROCESSED_DIR.glob("*_nav.csv")):
    df = pd.read_csv(file_path, parse_dates=["date"])

    future = df[df["date"] > TODAY]
    invalid_nav = df[df["nav"] <= 0]

    if not future.empty or not invalid_nav.empty:
        print("\n" + "=" * 55)
        print("File:", file_path.name)

        if not future.empty:
            print("\nFuture-dated records:")
            print(future[["date", "nav"]].to_string(index=False))

        if not invalid_nav.empty:
            print("\nNon-positive NAV records:")
            print(invalid_nav[["date", "nav"]].to_string(index=False))

print("\nInvestigation complete.")
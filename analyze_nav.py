

from pathlib import Path
import pandas as pd

PROCESSED_DIR = Path("data/processed")

results = []

for file_path in sorted(PROCESSED_DIR.glob("*_nav.csv")):
    df = pd.read_csv(file_path, parse_dates=["date"])
    df = df.sort_values("date")

    results.append({
        "file": file_path.name,
        "total_records": len(df),
        "first_date": df["date"].min().date(),
        "latest_date": df["date"].max().date(),
        "latest_nav": round(df["nav"].iloc[-1], 4),
        "average_nav": round(df["nav"].mean(), 4),
        "minimum_nav": round(df["nav"].min(), 4),
        "maximum_nav": round(df["nav"].max(), 4),
    })

report = pd.DataFrame(results)

Path("reports").mkdir(parents=True, exist_ok=True)
report.to_csv("reports/nav_analysis_summary.csv", index=False)

print("\nNAV Analysis Summary")
print(report.to_string(index=False))
print("\nSaved: reports/nav_analysis_summary.csv")

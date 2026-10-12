

from pathlib import Path
import pandas as pd

PROCESSED_DIR = Path("data/processed")
REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

periods = {
    "1_year_return_pct": 365,
    "3_year_return_pct": 365 * 3,
    "5_year_return_pct": 365 * 5,
}

results = []

for file_path in sorted(PROCESSED_DIR.glob("*_nav.csv")):
    df = pd.read_csv(file_path, parse_dates=["date"])
    df["nav"] = pd.to_numeric(df["nav"], errors="coerce")
    df = df.dropna(subset=["date", "nav"])
    df = df[df["nav"] > 0].sort_values("date")

    if df.empty:
        continue

    latest = df.iloc[-1]
    row = {
        "file": file_path.name,
        "latest_date": latest["date"].date(),
        "latest_nav": latest["nav"],
    }

    for label, days in periods.items():
        target_date = latest["date"] - pd.Timedelta(days=days)
        eligible = df[df["date"] <= target_date]

        if eligible.empty:
            row[label] = None
        else:
            past_nav = eligible.iloc[-1]["nav"]
            row[label] = round((latest["nav"] / past_nav - 1) * 100, 2)

    results.append(row)

report = pd.DataFrame(results)
output = REPORT_DIR / "historical_returns.csv"
report.to_csv(output, index=False)

print("\nHistorical NAV Returns (%)")
print(report.to_string(index=False))
print(f"\nSaved: {output}")

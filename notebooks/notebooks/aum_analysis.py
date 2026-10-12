

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_DIR / "data" / "raw"
REPORT_DIR = PROJECT_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

files = list(RAW_DIR.glob("*03_aum_by_fund_house.csv"))

if not files:
    raise FileNotFoundError("AUM dataset not found in data/raw")

df = pd.read_csv(files[0])
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# Latest available AUM for each fund house
latest_date = df["date"].max()
latest = df[df["date"] == latest_date].sort_values(
    "aum_crore", ascending=False
)

print("Latest AUM date:", latest_date.date())
print("\nAUM by fund house (₹ crore):")
print(latest[["fund_house", "aum_crore"]].to_string(index=False))

latest.to_csv(REPORT_DIR / "latest_aum_by_fund_house.csv", index=False)

# Plot the latest available AUM
plt.figure(figsize=(11, 6))
plt.bar(latest["fund_house"], latest["aum_crore"])
plt.title(f"AUM by Fund House — {latest_date.date()}")
plt.xlabel("Fund House")
plt.ylabel("AUM (₹ crore)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(REPORT_DIR / "aum_by_fund_house.png", dpi=150)
plt.show()

print("\nSaved AUM summary and chart in reports/")



from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_DIR / "data" / "raw"
REPORT_DIR = PROJECT_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

files = list(RAW_DIR.glob("*07_scheme_performance.csv"))

if not files:
    raise FileNotFoundError("Scheme performance dataset not found")

df = pd.read_csv(files[0])

# Rank schemes by their supplied 5-year return
top_funds = df.sort_values(
    "return_5yr_pct", ascending=False
).head(10)

print("\nTop 10 schemes by supplied 5-year return:")
print(
    top_funds[
        ["scheme_name", "category", "return_5yr_pct",
         "return_3yr_pct", "return_1yr_pct"]
    ].to_string(index=False)
)

top_funds.to_csv(
    REPORT_DIR / "top_10_funds_by_5yr_return.csv",
    index=False
)

plt.figure(figsize=(12, 6))
plt.barh(
    top_funds["scheme_name"].iloc[::-1],
    top_funds["return_5yr_pct"].iloc[::-1]
)
plt.title("Top 10 Schemes by Supplied 5-Year Return")
plt.xlabel("5-year return (%)")
plt.ylabel("Scheme")
plt.tight_layout()
plt.savefig(
    REPORT_DIR / "top_10_funds_by_5yr_return.png",
    dpi=150
)
plt.show()

print("\nPerformance report and chart saved in reports/")

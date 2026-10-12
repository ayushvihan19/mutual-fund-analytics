

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_DIR / "data" / "raw"
REPORT_DIR = PROJECT_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

files = list(RAW_DIR.glob("*category_inflows.csv"))

if not files:
    raise FileNotFoundError("Category inflows dataset not found.")

df = pd.read_csv(files[0])

# Total net inflow for each category across all available months
category_totals = (
    df.groupby("category")["net_inflow_crore"]
    .sum()
    .sort_values(ascending=False)
)

print("Total net inflows by category (₹ crore):")
print(category_totals.round(2).to_string())

print("\nHighest total inflow category:")
print(category_totals.index[0])

category_totals.to_csv(
    REPORT_DIR / "category_inflow_summary.csv",
    header=["total_net_inflow_crore"]
)

category_totals.plot(kind="bar", figsize=(10, 5))
plt.title("Total Net Inflows by Mutual Fund Category")
plt.xlabel("Category")
plt.ylabel("Net inflow (₹ crore)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(REPORT_DIR / "category_inflows.png", dpi=150)
plt.show()

print("\nSaved category summary and chart in reports/")

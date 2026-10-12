

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_DIR / "data" / "raw"
REPORT_DIR = PROJECT_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

files = list(RAW_DIR.glob("*08_investor_transactions*.csv"))

if not files:
    raise FileNotFoundError("Investor transactions dataset not found")

df = pd.read_csv(files[0])

# Summarize transaction types
summary = (
    df.groupby("transaction_type")
    .agg(
        transaction_count=("transaction_type", "size"),
        total_amount_inr=("amount_inr", "sum")
    )
    .sort_values("total_amount_inr", ascending=False)
)

print("\nTransaction summary:")
print(summary.to_string())

summary.to_csv(REPORT_DIR / "investor_transaction_summary.csv")

# Chart transaction counts
summary["transaction_count"].sort_values().plot(
    kind="barh", figsize=(9, 5)
)
plt.title("Number of Transactions by Type")
plt.xlabel("Number of transactions")
plt.ylabel("Transaction type")
plt.tight_layout()
plt.savefig(
    REPORT_DIR / "investor_transactions_by_type.png",
    dpi=150
)
plt.show()

# Top 10 cities by total transaction amount
city_summary = (
    df.groupby("city")["amount_inr"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 cities by transaction amount:")
print(city_summary.to_string())

city_summary.to_csv(REPORT_DIR / "top_10_cities_by_amount.csv")

print("\nReports saved in the reports folder.")

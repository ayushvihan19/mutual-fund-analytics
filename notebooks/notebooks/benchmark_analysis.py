

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_DIR / "data" / "raw"
REPORT_DIR = PROJECT_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

files = list(RAW_DIR.glob("*10_benchmark_indices.csv"))

if not files:
    raise FileNotFoundError("Benchmark indices dataset not found")

df = pd.read_csv(files[0])

# Clean and prepare the data
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["close_value"] = pd.to_numeric(df["close_value"], errors="coerce")

df = df.dropna(subset=["date", "index_name", "close_value"])
df = df[df["close_value"] > 0]
df = df.sort_values(["index_name", "date"])
df = df.drop_duplicates(subset=["index_name", "date"], keep="last")

# Calculate percentage change for each index
df["daily_return_pct"] = (
    df.groupby("index_name")["close_value"].pct_change() * 100
)

# Calculate overall change from first to last available observation
summary = df.groupby("index_name").agg(
    first_date=("date", "min"),
    latest_date=("date", "max"),
    first_close=("close_value", "first"),
    latest_close=("close_value", "last"),
    observations=("close_value", "count"),
).reset_index()

summary["overall_change_pct"] = (
    (summary["latest_close"] / summary["first_close"] - 1) * 100
)

summary.to_csv(REPORT_DIR / "benchmark_return_summary.csv", index=False)
df.to_csv(REPORT_DIR / "benchmark_returns_daily.csv", index=False)

print("\nBenchmark Return Summary:")
print(summary.to_string(index=False))

print("\nSaved files:")
print("reports/benchmark_return_summary.csv")
print("reports/benchmark_returns_daily.csv")


# Create benchmark comparison chart
chart_data = summary.sort_values("overall_change_pct")

plt.figure(figsize=(10, 6))
plt.barh(
    chart_data["index_name"],
    chart_data["overall_change_pct"]
)
plt.title("Benchmark Indices: Overall Percentage Change")
plt.xlabel("Overall change (%)")
plt.ylabel("Benchmark index")
plt.tight_layout()

chart_path = REPORT_DIR / "benchmark_comparison.png"
plt.savefig(chart_path, dpi=150)
plt.show()

print(f"\nChart saved to: {chart_path}")

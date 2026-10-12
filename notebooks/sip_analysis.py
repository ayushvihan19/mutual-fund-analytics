

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_DIR / "data" / "raw"
REPORT_DIR = PROJECT_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

files = list(RAW_DIR.glob("*monthly_sip_inflows.csv"))

if not files:
    raise FileNotFoundError("Monthly SIP dataset not found in data/raw")

df = pd.read_csv(files[0])
df["month"] = pd.to_datetime(df["month"], format="%Y-%m")
df = df.sort_values("month")

df["inflow_change_pct"] = df["sip_inflow_crore"].pct_change() * 100

highest = df.loc[df["sip_inflow_crore"].idxmax()]
lowest = df.loc[df["sip_inflow_crore"].idxmin()]

print("Highest SIP inflow:")
print(highest[["month", "sip_inflow_crore"]].to_string())

print("\nLowest SIP inflow:")
print(lowest[["month", "sip_inflow_crore"]].to_string())

print("\nAverage monthly SIP inflow:",
      round(df["sip_inflow_crore"].mean(), 2), "crore")

print("\nMissing YoY growth values:",
      df["yoy_growth_pct"].isna().sum())

df.to_csv(REPORT_DIR / "sip_analysis.csv", index=False)

plt.figure(figsize=(12, 5))
plt.plot(df["month"], df["sip_inflow_crore"], marker="o")
plt.title("Monthly SIP Inflows Over Time")
plt.xlabel("Month")
plt.ylabel("SIP Inflow (₹ crore)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(REPORT_DIR / "monthly_sip_inflows.png", dpi=150)
plt.show()

print("\nAnalysis CSV and chart saved in the reports folder.")

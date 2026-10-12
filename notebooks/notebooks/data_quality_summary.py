

from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_DIR / "data" / "raw"
REPORT_DIR = PROJECT_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

fund_file = list(RAW_DIR.glob("*01_fund_master.csv"))[0]
nav_file = list(RAW_DIR.glob("*02_nav_history.csv"))[0]

funds = pd.read_csv(fund_file)
nav = pd.read_csv(nav_file)

fund_codes = set(pd.to_numeric(
    funds["amfi_code"], errors="coerce"
).dropna())

nav_codes = set(pd.to_numeric(
    nav["amfi_code"], errors="coerce"
).dropna())

summary = pd.DataFrame([
    {
        "check": "Fund master row count",
        "result": len(funds),
        "status": "INFO"
    },
    {
        "check": "NAV history row count",
        "result": len(nav),
        "status": "INFO"
    },
    {
        "check": "Unique fund master AMFI codes",
        "result": len(fund_codes),
        "status": "INFO"
    },
    {
        "check": "Fund master codes missing from NAV history",
        "result": len(fund_codes - nav_codes),
        "status": "PASS" if not (fund_codes - nav_codes) else "CHECK"
    },
    {
        "check": "NAV history codes not in fund master",
        "result": len(nav_codes - fund_codes),
        "status": "INFO"
    },
    {
        "check": "Missing values in fund master",
        "result": int(funds.isna().sum().sum()),
        "status": "CHECK" if funds.isna().sum().sum() else "PASS"
    },
    {
        "check": "Missing values in NAV history",
        "result": int(nav.isna().sum().sum()),
        "status": "CHECK" if nav.isna().sum().sum() else "PASS"
    },
])

output_file = REPORT_DIR / "data_quality_summary.csv"
summary.to_csv(output_file, index=False)

print("\nDATA QUALITY SUMMARY")
print(summary.to_string(index=False))
print(f"\nSaved: {output_file}")

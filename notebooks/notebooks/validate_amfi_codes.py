

from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_DIR / "data" / "raw"
REPORT_DIR = PROJECT_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

fund_files = list(RAW_DIR.glob("*01_fund_master.csv"))
nav_files = list(RAW_DIR.glob("*02_nav_history.csv"))

if not fund_files:
    raise FileNotFoundError("Fund master dataset not found")

if not nav_files:
    raise FileNotFoundError("NAV history dataset not found")

funds = pd.read_csv(fund_files[0])
nav = pd.read_csv(nav_files[0])

funds["amfi_code"] = pd.to_numeric(
    funds["amfi_code"], errors="coerce"
)
nav["amfi_code"] = pd.to_numeric(
    nav["amfi_code"], errors="coerce"
)

nav_codes = set(nav["amfi_code"].dropna().unique())

funds["exists_in_nav_history"] = funds["amfi_code"].isin(nav_codes)

print("Total schemes in fund master:", len(funds))
print("Codes found in NAV history:",
      int(funds["exists_in_nav_history"].sum()))
print("Codes missing from NAV history:",
      int((~funds["exists_in_nav_history"]).sum()))

print("\nMissing scheme codes:")
print(
    funds.loc[
        ~funds["exists_in_nav_history"],
        ["amfi_code", "fund_house", "scheme_name"]
    ].to_string(index=False)
)

funds.to_csv(
    REPORT_DIR / "amfi_code_validation.csv",
    index=False
)

print("\nSaved: reports/amfi_code_validation.csv")



from pathlib import Path
import pandas as pd

# Project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_DIR / "data" / "raw"
REPORT_DIR = PROJECT_DIR / "reports"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

# The 10 main internship datasets
datasets = [
    "investor_transactions",
    "portfolio_holdings",
    "benchmark_indices",
    "fund_master",
    "nav_history",
    "aum_by_fund_house",
    "monthly_sip_inflows",
    "category_inflows",
    "industry_folio_count",
    "scheme_performance",
]

results = []

for keyword in datasets:
    matches = [
        file for file in RAW_DIR.glob("*.csv")
        if keyword in file.name.lower()
        and "_nav.csv" not in file.name.lower()
    ]

    if not matches:
        print(f"\nDataset not found: {keyword}")
        continue

    file = matches[0]
    df = pd.read_csv(file)

    print("\n" + "=" * 55)
    print("DATASET:", file.name)
    print("Rows and columns:", df.shape)

    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nData types:")
    print(df.dtypes.to_string())

    print("\nMissing values:")
    print(df.isnull().sum().to_string())

    print("\nDuplicate rows:", df.duplicated().sum())

    print("\nFirst 3 rows:")
    print(df.head(3).to_string(index=False))

    results.append({
        "dataset": file.name,
        "rows": len(df),
        "columns": len(df.columns),
        "missing_cells": int(df.isnull().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
    })

summary = pd.DataFrame(results)
output_file = REPORT_DIR / "eda_summary.csv"
summary.to_csv(output_file, index=False)

print("\nEDA SUMMARY")
print(summary.to_string(index=False))
print(f"\nSaved report to: {output_file}")

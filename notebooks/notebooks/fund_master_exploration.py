

from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_DIR / "data" / "raw"

files = list(RAW_DIR.glob("*01_fund_master.csv"))

if not files:
    raise FileNotFoundError("Fund master CSV not found in data/raw")

df = pd.read_csv(files[0])

print("\nFund master shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())

# Find likely columns for fund house, category, sub-category and risk
for keyword in ["house", "category", "sub", "risk"]:
    matching_columns = [
        col for col in df.columns
        if keyword in col.lower()
    ]

    for col in matching_columns:
        print(f"\nUnique values in '{col}':")
        print(df[col].dropna().unique())

# Check scheme codes
code_columns = [
    col for col in df.columns
    if "code" in col.lower()
]

for col in code_columns:
    print(f"\nSample values from '{col}':")
    print(df[col].head(10).to_list())


from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

def inspect_csv(file_path):
    print("\n" + "=" * 60)
    print(f"FILE: {file_path.name}")
    
    try:
        df = pd.read_csv(file_path)
        print("Shape:", df.shape)
        print("\nData types:")
        print(df.dtypes)
        print("\nFirst 5 rows:")
        print(df.head())
        
        print("\nMissing values:")
        print(df.isnull().sum())
        
        print("\nDuplicate rows:", df.duplicated().sum())
        
        return df

    except Exception as error:
        print(f"Could not read file: {error}")
        return None

def main():
    csv_files = sorted(RAW_DIR.glob("*.csv"))

    if not csv_files:
        print("No CSV files found in data/raw.")
        return

    print(f"Found {len(csv_files)} CSV files.")

    for file_path in csv_files:
        inspect_csv(file_path)

    print("\nInspection complete.")

if __name__ == "__main__":
    main()
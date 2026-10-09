
import requests
import pandas as pd
from pathlib import Path
import time

# Project folder
RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

# Verified codes so far.
# HDFC and SBI are left out until their codes are confirmed.
FUNDS = {
    "ICICI Prudential Large Cap": 120586,
    "Nippon India Large Cap": 118632,
    "Axis Large Cap": 120465,
    "Kotak Large Cap": 120152,
}

def fetch_nav(fund_name, scheme_code):
    url = f"https://api.mfapi.in/mf/{scheme_code}"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()

        actual_name = data.get("meta", {}).get("scheme_name", "")
        records = data.get("data", [])

        if not records:
            print(f"⚠️ No NAV records: {fund_name}")
            return

        print(f"\nRequested: {fund_name}")
        print(f"API name:  {actual_name}")

        # Save only after displaying the actual scheme name
        df = pd.DataFrame(records)
        df["date"] = pd.to_datetime(
            df["date"], format="%d-%m-%Y", errors="coerce"
        )
        df["nav"] = pd.to_numeric(df["nav"], errors="coerce")
        df = df.dropna(subset=["date", "nav"])
        df = df.sort_values("date")

        filename = RAW_DIR / f"{scheme_code}_nav.csv"
        df.to_csv(filename, index=False)

        print(f"Saved: {filename}")
        print(f"Valid NAV records: {len(df)}")

    except requests.RequestException as error:
        print(f"❌ API/network error for {fund_name}: {error}")
    except (ValueError, KeyError) as error:
        print(f"❌ Invalid API response for {fund_name}: {error}")

for name, code in FUNDS.items():
    fetch_nav(name, code)
    time.sleep(1)

print("\nNAV download process finished.")


from pathlib import Path
import requests
import pandas as pd

# Main project folder
PROJECT_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_DIR / "data" / "raw"
REPORT_DIR = PROJECT_DIR / "reports"

RAW_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

scheme_codes = {
    "125497": "HDFC Top 100 Direct",
    "119551": "SBI Bluechip",
    "120503": "ICICI Bluechip",
    "118632": "Nippon Large Cap",
    "119092": "Axis Bluechip",
    "120841": "Kotak Bluechip",
}

results = []

for code, expected_name in scheme_codes.items():
    print(f"\n{'=' * 50}")
    print(f"Checking {code}: {expected_name}")

    try:
        response = requests.get(
            f"https://api.mfapi.in/mf/{code}",
            timeout=30
        )
        response.raise_for_status()
        data = response.json()

        meta = data.get("meta") or {}
        actual_name = meta.get("scheme_name", "Unknown")
        nav_data = data.get("data", [])

        print("Actual scheme:", actual_name)
        print("NAV records:", len(nav_data))

        # Flexible name check
        expected_words = expected_name.lower().split()
        actual_lower = actual_name.lower()
        matches = all(word in actual_lower for word in expected_words)

        # Allow common variations in the Nippon fund name
        if code == "118632" and "nippon india large cap" in actual_lower:
            matches = True

        if matches and nav_data:
            df = pd.DataFrame(nav_data)
            df["scheme_code"] = code
            df["scheme_name"] = actual_name

            output_file = RAW_DIR / f"{code}_nav.csv"
            df.to_csv(output_file, index=False)
            status = "Verified name; NAV saved"
            print("Saved:", output_file)
        else:
            status = "Name mismatch or no NAV data; skipped"
            print("WARNING:", status)

        results.append({
            "scheme_code": code,
            "expected_name": expected_name,
            "actual_name": actual_name,
            "nav_records": len(nav_data),
            "name_match": matches,
            "status": status
        })

    except Exception as error:
        print("ERROR:", error)
        results.append({
            "scheme_code": code,
            "expected_name": expected_name,
            "actual_name": "Unknown",
            "nav_records": 0,
            "name_match": False,
            "status": str(error)
        })

report = pd.DataFrame(results)
report_path = REPORT_DIR / "nav_code_verification.csv"
report.to_csv(report_path, index=False)

print("\nVerification summary:")
print(report.to_string(index=False))
print(f"\nReport saved: {report_path}")

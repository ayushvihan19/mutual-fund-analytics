
from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw")
REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

TODAY = pd.Timestamp.today().normalize()
issues = []

for file_path in sorted(RAW_DIR.glob("*_nav.csv")):
    df = pd.read_csv(file_path)

    df["date"] = pd.to_datetime(
        df["date"], format="mixed", dayfirst=True, errors="coerce"
    )
    df["nav"] = pd.to_numeric(df["nav"], errors="coerce")

    checks = [
        ("invalid_date", df["date"].isna()),
        ("invalid_nav", df["nav"].isna()),
        ("non_positive_nav", df["nav"].le(0)),
        ("future_date", df["date"].gt(TODAY)),
        ("duplicate_date", df["date"].duplicated(keep=False)),
    ]

    for issue_type, mask in checks:
        for _, row in df.loc[mask].iterrows():
            issues.append({
                "file": file_path.name,
                "issue": issue_type,
                "date": row["date"],
                "nav": row["nav"],
            })

    print(
        f"{file_path.name}: {len(df)} rows, "
        f"{sum(mask.sum() for _, mask in checks)} issue flags"
    )

report = pd.DataFrame(
    issues, columns=["file", "issue", "date", "nav"]
)
report.to_csv(REPORT_DIR / "data_quality_issues.csv", index=False)

summary = (
    report.groupby(["file", "issue"]).size().rename("count").reset_index()
    if not report.empty
    else pd.DataFrame(columns=["file", "issue", "count"])
)

summary.to_csv(REPORT_DIR / "data_quality_summary.csv", index=False)

print("\nSaved:")
print("reports/data_quality_issues.csv")
print("reports/data_quality_summary.csv")
print("\nIssue counts:")
print(summary.to_string(index=False))
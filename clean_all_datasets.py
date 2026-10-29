

from pathlib import Path
import pandas as pd

RAW = Path("data/raw")
OUT = Path("data/processed")
OUT.mkdir(parents=True, exist_ok=True)

files = {
    "fund_master": "*-01_fund_master.csv",
    "nav_history": "*-02_nav_history.csv",
    "aum_by_fund_house": "*-03_aum_by_fund_house.csv",
    "monthly_sip_inflows": "*-04_monthly_sip_inflows.csv",
    "category_inflows": "*-05_category_inflows.csv",
    "industry_folio_count": "*-06_industry_folio_count.csv",
    "scheme_performance": "*-07_scheme_performance.csv",
    "investor_transactions": "*_investor_transactions*.csv",
    "portfolio_holdings": "*-09_portfolio_holdings.csv",
    "benchmark_indices": "*-10_benchmark_indices.csv",
}

def clean_file(name, pattern):
    matches = list(RAW.glob(pattern))

    if not matches:
        print(f"SKIPPED: {name} - source file not found")
        return

    source = matches[0]
    df = pd.read_csv(source)
    original_rows = len(df)
    df = df.drop_duplicates().copy()

    date_cols = [
        "date", "transaction_date", "portfolio_date",
        "launch_date", "month"
    ]

    for col in date_cols:
        if col in df.columns:
            parsed = pd.to_datetime(
                df[col], errors="coerce", format="mixed"
            )
            valid = parsed.notna()
            df = df.loc[valid].copy()
            df[col] = parsed.loc[valid].dt.strftime("%Y-%m-%d")

    numeric_cols = [
        "amfi_code", "nav", "amount_inr", "expense_ratio_pct",
        "exit_load_pct", "min_sip_amount", "min_lumpsum_amount",
        "aum_lakh_crore", "aum_crore", "num_schemes",
        "sip_inflow_crore", "active_sip_accounts_crore",
        "new_sip_accounts_lakh", "sip_aum_lakh_crore",
        "yoy_growth_pct", "net_inflow_crore",
        "total_folios_crore", "equity_folios_crore",
        "debt_folios_crore", "hybrid_folios_crore",
        "others_folios_crore", "return_1yr_pct",
        "return_3yr_pct", "return_5yr_pct",
        "benchmark_3yr_pct", "alpha", "beta", "sharpe_ratio",
        "sortino_ratio", "std_dev_ann_pct", "max_drawdown_pct",
        "morningstar_rating", "weight_pct", "market_value_cr",
        "current_price_inr", "close_value"
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "nav" in df.columns:
        df = df.dropna(subset=["nav"])
        df = df[df["nav"] > 0]

        if {"amfi_code", "date"}.issubset(df.columns):
            df = df.drop_duplicates(
                subset=["amfi_code", "date"], keep="last"
            )
            df = df.sort_values(["amfi_code", "date"])

    if "amount_inr" in df.columns:
        df = df.dropna(subset=["amount_inr"])
        df = df[df["amount_inr"] > 0]

        if "transaction_type" in df.columns:
            df["transaction_type"] = (
                df["transaction_type"].astype(str).str.strip().str.title()
            )
            df["transaction_type"] = df["transaction_type"].replace({
                "Lump Sum": "Lumpsum",
                "Lump-Sum": "Lumpsum"
            })

        if "kyc_status" in df.columns:
            df["kyc_status"] = (
                df["kyc_status"].astype(str).str.strip().str.upper()
            )

    if "expense_ratio_pct" in df.columns:
        df["expense_ratio_valid"] = df["expense_ratio_pct"].between(
            0.1, 2.5, inclusive="both"
        )

    output = OUT / f"{name}_cleaned.csv"
    df.to_csv(output, index=False)

    print(
        f"OK: {name} | source rows={original_rows} | "
        f"cleaned rows={len(df)} | saved={output}"
    )


def main():
    for name, pattern in files.items():
        clean_file(name, pattern)

    print("\nCleaning run finished.")


if __name__ == "__main__":
    main()

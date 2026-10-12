
# Mutual Fund Analytics

## 1. Project Overview
This project analyzes mutual fund data using Python and data analytics techniques. It focuses on NAV history, fund performance, investor transactions, SIP inflows, assets under management (AUM), and benchmark indices.

## 2. Project Objectives
- Load and inspect mutual fund datasets.
- Clean and validate NAV data.
- Perform exploratory data analysis (EDA).
- Calculate historical NAV returns.
- Analyze SIP and category-wise inflows.
- Study investor transaction patterns.
- Compare benchmark index performance.
- Generate reports and visualizations.

## 3. Technologies Used
- Python
- pandas
- NumPy
- Matplotlib
- Seaborn
- SQL
- Git and GitHub

## 4. Project Structure
```text
mutual-fund-analytics/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── sql/
├── dashboard/
├── reports/
├── data_ingestion.py
├── clean_nav_data.py
├── analyze_nav.py
├── calculate_returns.py
├── live_nav_fetch.py
├── requirements.txt
└── README.md
```

## 5. Analysis Completed
- Data ingestion and dataset inspection
- Data quality checks
- NAV data cleaning
- Historical NAV analysis and returns
- SIP inflow analysis
- Category-wise inflow analysis
- AUM analysis by fund house
- Investor transaction analysis
- Top funds by reported five-year return
- Benchmark index comparison
- AMFI code validation

## 6. Reports Generated
The `reports/` directory contains CSV summaries and charts for data quality, NAV analysis, historical returns, SIP inflows, category inflows, AUM, investor transactions, fund performance, and benchmark comparisons.

## 7. Data Quality
The supplied fund master contains 40 records, and the supplied NAV history contains 46,000 records. The validation script found all 40 fund-master AMFI codes in the NAV history, with no missing values in either of these two datasets.

Some live NAV API requests returned scheme names that did not match the expected funds. These mappings require further verification.

## 8. How to Run the Project

Create and activate a virtual environment in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run the main scripts from the project root:

```powershell
python data_ingestion.py
python clean_nav_data.py
python analyze_nav.py
python calculate_returns.py
python notebooks/eda_analysis.py
```

Additional analysis scripts are available under `notebooks/notebooks/`.

## 9. Limitations
- Results depend on the supplied datasets and analysis periods.
- Live NAV scheme mappings require verification.
- Historical performance does not guarantee future returns.
- This project is for educational and analytical purposes, not investment advice.

## 10. Conclusion
This project demonstrates practical data analytics skills, including data ingestion, cleaning, validation, exploratory analysis, return calculations, and visualization of mutual fund-related datasets.

## Author
Data Analyst Internship Project

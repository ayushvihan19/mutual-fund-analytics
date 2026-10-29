\# Mutual Fund Analytics — Data Dictionary



\## Project Overview

This project analyzes mutual fund data using Python, CSV datasets, SQLite, and SQL queries. It covers fund information, NAV history, investor transactions, portfolio holdings, fund performance, and assets under management (AUM).



\## Dataset Tables



| Table | Description |

|---|---|

| fund\_master | Mutual fund scheme details, category, fund house, plan, and expense ratio. |

| nav\_history | Historical Net Asset Value (NAV) for mutual fund schemes. |

| investor\_transactions | Investor transaction records, amounts, dates, and transaction types. |

| portfolio\_holdings | Stocks held by mutual fund schemes, sectors, weights, and market values. |

| benchmark\_indices | Historical closing values of market benchmark indices. |

| scheme\_performance | Scheme returns, risk measures, ratings, and AUM. |

| aum\_by\_fund\_house | Assets under management and scheme counts by fund house and date. |

| monthly\_sip\_inflows | Monthly Systematic Investment Plan (SIP) inflow statistics. |

| category\_inflows | Monthly net inflows by mutual fund category. |

| industry\_folio\_count | Monthly mutual fund folio counts across categories. |



\## Important Columns



\### Fund Master

\- `amfi\_code`: Unique scheme identifier.

\- `scheme\_name`: Name of the mutual fund scheme.

\- `fund\_house`: Asset management company or fund house.

\- `category`: Broad mutual fund category.

\- `sub\_category`: More specific scheme classification.

\- `expense\_ratio\_pct`: Scheme expense ratio in percentage.

\- `risk\_category`: Reported risk classification.



\### NAV History

\- `amfi\_code`: Mutual fund scheme identifier.

\- `date`: NAV observation date.

\- `nav`: Net Asset Value; should be greater than zero.



\### Investor Transactions

\- `investor\_id`: Investor identifier.

\- `transaction\_date`: Date of the transaction.

\- `amfi\_code`: Related mutual fund scheme identifier.

\- `transaction\_type`: Type of transaction.

\- `amount\_inr`: Transaction amount in Indian rupees.

\- `state`, `city`: Investor location fields.

\- `payment\_mode`: Payment method used.

\- `kyc\_status`: Know Your Customer verification status.



\### Scheme Performance

\- `return\_1yr\_pct`, `return\_3yr\_pct`, `return\_5yr\_pct`: Reported returns over different periods.

\- `benchmark\_3yr\_pct`: Benchmark return over three years.

\- `alpha`, `beta`: Performance and market-risk measures.

\- `sharpe\_ratio`, `sortino\_ratio`: Risk-adjusted performance measures.

\- `aum\_crore`: Assets under management in crore rupees.

\- `risk\_grade`: Reported risk grade.



\## Data Quality Rules

\- Check for missing values in important fields.

\- Check for duplicate records using appropriate business keys.

\- NAV values must be positive.

\- Transaction amounts must be positive.

\- Dates should use a consistent format.

\- Verify primary and foreign key relationships when loading the database.



\## Database Notes

The current SQLite database contains 10 source tables. `sql/schema.sql` defines a proposed analytical star schema. The dimension and fact tables must be populated and validated before the star schema can be considered complete.




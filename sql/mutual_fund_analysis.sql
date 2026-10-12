

-- 1. Top funds by reported 5-year return
SELECT scheme_name, return_5yr_pct
FROM scheme_performance
ORDER BY return_5yr_pct DESC
LIMIT 10;

-- 2. Total transactions by transaction type
SELECT transaction_type,
       COUNT(*) AS transaction_count,
       SUM(amount) AS total_amount
FROM investor_transactions
GROUP BY transaction_type
ORDER BY total_amount DESC;

-- 3. Monthly SIP inflow trend
SELECT year, month, sip_inflow_crore
FROM monthly_sip_inflows
ORDER BY year, month;

-- 4. Latest AUM by fund house
SELECT fund_house, report_date, aum_crore
FROM aum_by_fund_house
ORDER BY report_date DESC, aum_crore DESC;

-- 5. Fund count by category
SELECT category, COUNT(*) AS fund_count
FROM fund_master
GROUP BY category
ORDER BY fund_count DESC;

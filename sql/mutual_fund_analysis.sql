

-- 1. Top funds by reported 5-year return
SELECT scheme_name, return_5yr_pct
FROM scheme_performance
ORDER BY return_5yr_pct DESC
LIMIT 10;

-- 2. Transaction count and amount by type
SELECT transaction_type,
       COUNT(*) AS transaction_count,
       SUM(amount_inr) AS total_amount_inr
FROM investor_transactions
GROUP BY transaction_type
ORDER BY total_amount_inr DESC;

-- 3. Monthly SIP inflow trend
SELECT month, sip_inflow_crore
FROM monthly_sip_inflows
ORDER BY month;

-- 4. Latest AUM by fund house
SELECT fund_house, date, aum_crore
FROM aum_by_fund_house
WHERE date = (
    SELECT MAX(date) FROM aum_by_fund_house
)
ORDER BY aum_crore DESC;

-- 5. Fund count by category
SELECT category, COUNT(*) AS fund_count
FROM fund_master
GROUP BY category
ORDER BY fund_count DESC;

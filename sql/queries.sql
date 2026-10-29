
-- 1. Top 5 funds by AUM
SELECT amfi_code, scheme_name, fund_house, aum_crore
FROM scheme_performance
ORDER BY aum_crore DESC
LIMIT 5;

-- 2. Average NAV by month
SELECT substr(date, 1, 7) AS month,
       ROUND(AVG(nav), 4) AS average_nav
FROM nav_history
GROUP BY substr(date, 1, 7)
ORDER BY month;

-- 3. Monthly SIP inflow and YoY growth
SELECT month, sip_inflow_crore, yoy_growth_pct
FROM monthly_sip_inflows
ORDER BY month;

-- 4. Transaction count and amount by state
SELECT state, COUNT(*) AS transaction_count,
       SUM(amount_inr) AS total_amount_inr
FROM investor_transactions
GROUP BY state
ORDER BY total_amount_inr DESC;

-- 5. Funds with expense ratio below 1 percent
SELECT amfi_code, scheme_name, expense_ratio_pct
FROM scheme_performance
WHERE expense_ratio_pct < 1.0
ORDER BY expense_ratio_pct ASC;

-- 6. Transaction summary by transaction type
SELECT transaction_type, COUNT(*) AS transaction_count,
       SUM(amount_inr) AS total_amount_inr
FROM investor_transactions
GROUP BY transaction_type
ORDER BY total_amount_inr DESC;

-- 7. Fund count by category
SELECT category, COUNT(*) AS fund_count
FROM fund_master
GROUP BY category
ORDER BY fund_count DESC;

-- 8. Latest AUM by fund house
SELECT fund_house, date, aum_crore
FROM aum_by_fund_house
WHERE date = (SELECT MAX(date) FROM aum_by_fund_house)
ORDER BY aum_crore DESC;

-- 9. Top 10 funds by 5-year return
SELECT scheme_name, category, return_5yr_pct
FROM scheme_performance
WHERE return_5yr_pct IS NOT NULL
ORDER BY return_5yr_pct DESC
LIMIT 10;

-- 10. Portfolio holdings by sector
SELECT sector, COUNT(*) AS holding_count,
       ROUND(SUM(weight_pct), 2) AS total_weight_pct
FROM portfolio_holdings
GROUP BY sector
ORDER BY total_weight_pct DESC;

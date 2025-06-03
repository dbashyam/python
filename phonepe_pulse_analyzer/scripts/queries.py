# scripts/queries.py

QUERY_TOP_STATES_TRANSACTIONS_2023 = """
SELECT state, SUM(count) AS total_transactions, SUM(amount) AS total_amount
FROM aggregated_transaction
WHERE year = 2023
GROUP BY state
ORDER BY total_transactions DESC
LIMIT 10;
"""
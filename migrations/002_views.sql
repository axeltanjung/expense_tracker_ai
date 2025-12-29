CREATE OR REPLACE VIEW spend_30d AS
SELECT user_id, SUM(amount) AS spend
FROM transactions
WHERE direction='out'
AND datetime >= now() - interval '30 day'
GROUP BY user_id;

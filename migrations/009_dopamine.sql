CREATE OR REPLACE VIEW dopamine_spend AS
SELECT user_id, COUNT(*) cnt, AVG(amount) avg_amt
FROM transactions
WHERE direction='out' AND amount < 100000
  AND datetime >= now()-interval '7 day'
GROUP BY user_id
HAVING COUNT(*) >= 10;

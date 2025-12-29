CREATE OR REPLACE VIEW spend_7d AS
SELECT user_id, SUM(amount) AS spend_7d
FROM transactions
WHERE direction='out'
AND datetime >= now() - interval '7 day'
GROUP BY user_id;

CREATE OR REPLACE VIEW spend_90d AS
SELECT user_id, SUM(amount) AS spend_90d
FROM transactions
WHERE direction='out'
AND datetime >= now() - interval '90 day'
GROUP BY user_id;

CREATE OR REPLACE VIEW cash_velocity AS
SELECT user_id,
       SUM(CASE WHEN direction='in' THEN amount ELSE 0 END)
     - SUM(CASE WHEN direction='out' THEN amount ELSE 0 END) AS net_30d
FROM transactions
WHERE datetime >= now() - interval '30 day'
GROUP BY user_id;

CREATE OR REPLACE VIEW subscriptions_detect AS
SELECT merchant,
       COUNT(*) AS cnt,
       AVG(amount) AS avg_amt,
       STDDEV(amount) AS std_amt
FROM transactions
WHERE direction='out'
GROUP BY merchant
HAVING COUNT(*) >= 3
   AND STDDEV(amount) < AVG(amount) * 0.15;

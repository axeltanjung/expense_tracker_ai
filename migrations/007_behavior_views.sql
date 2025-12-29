CREATE OR REPLACE VIEW lifestyle_creep AS
SELECT
  user_id,
  (SELECT SUM(amount) FROM transactions
    WHERE direction='out' AND datetime >= now()-interval '30 day' AND user_id=t.user_id) /
  (SELECT NULLIF(SUM(amount),1) FROM transactions
    WHERE direction='out' AND datetime BETWEEN now()-interval '60 day' AND now()-interval '30 day' AND user_id=t.user_id)
  AS creep_ratio
FROM transactions t
GROUP BY user_id;

CREATE TABLE regret_events(
  id SERIAL PRIMARY KEY,
  user_id UUID,
  txn_id UUID,
  created_at TIMESTAMPTZ DEFAULT now()
);

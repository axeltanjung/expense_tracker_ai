CREATE TABLE delayed_purchases (
  id SERIAL PRIMARY KEY,
  user_id UUID,
  merchant TEXT,
  amount NUMERIC,
  created_at TIMESTAMPTZ DEFAULT now(),
  status TEXT DEFAULT 'PENDING' -- PENDING / CONFIRMED / DROPPED
);

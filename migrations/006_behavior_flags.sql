CREATE TABLE behavior_flags (
  id SERIAL PRIMARY KEY,
  user_id UUID,
  date DATE,
  flag_type TEXT,       -- LIFESTYLE_CREEP, IMPULSE_BUY, SUBSCRIPTION_WASTE
  severity INT,        -- 1–5
  message TEXT,
  created_at TIMESTAMP DEFAULT now()
);

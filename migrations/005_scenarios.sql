CREATE TABLE scenarios (
  id SERIAL PRIMARY KEY,
  user_id UUID,
  name TEXT,
  extra_monthly_cost NUMERIC,
  created_at TIMESTAMP DEFAULT now()
);

CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE users (
  user_id UUID PRIMARY KEY,
  email TEXT UNIQUE,
  base_currency TEXT
);

CREATE TABLE categories (
  category_id SERIAL PRIMARY KEY,
  parent_id INT,
  name TEXT
);

CREATE TABLE transactions (
  txn_id UUID,
  user_id UUID,
  datetime TIMESTAMPTZ NOT NULL,
  amount NUMERIC,
  direction TEXT,
  merchant TEXT,
  PRIMARY KEY (txn_id, datetime)
);

SELECT create_hypertable('transactions', 'datetime');


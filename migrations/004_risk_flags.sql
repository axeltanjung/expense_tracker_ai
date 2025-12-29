CREATE TABLE risk_flags (
    id SERIAL PRIMARY KEY,
    user_id UUID,
    date DATE,
    flag_type TEXT,        -- FORECAST_RISK / ANOMALY_SPEND
    severity INT,          -- 1–5
    message TEXT,
    created_at TIMESTAMP DEFAULT now()
);
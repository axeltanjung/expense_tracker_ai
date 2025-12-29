import pandas as pd
from prophet import Prophet
from backend.db import engine

def run_forecast(user_id: str):
    df = pd.read_sql(f"""
        SELECT datetime::date as ds,
               SUM(CASE WHEN direction='in' THEN amount ELSE -amount END) AS y
        FROM transactions
        WHERE user_id='{user_id}'
        GROUP BY ds
        ORDER BY ds
    """, engine)

    if len(df) < 10:
        return

    model = Prophet()
    model.fit(df)

    future = model.make_future_dataframe(periods=30)
    fc = model.predict(future)

    min_future = fc.tail(30)['yhat'].min()

    if min_future < 0:
        engine.execute(f"""
            INSERT INTO risk_flags(user_id, date, flag_type, severity, message)
            VALUES ('{user_id}', CURRENT_DATE, 'FORECAST_RISK', 4,
            'Cashflow dip forecasted in next 30 days')
        """)

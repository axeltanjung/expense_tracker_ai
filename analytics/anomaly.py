import pandas as pd
from sklearn.ensemble import IsolationForest
from backend.db import engine

def run_anomaly(user_id: str):
    df = pd.read_sql(f"""
        SELECT datetime::date as ds, amount
        FROM transactions
        WHERE user_id='{user_id}' AND direction='out'
        ORDER BY ds
    """, engine)

    if len(df) < 20:
        return

    model = IsolationForest(contamination=0.03)
    df['flag'] = model.fit_predict(df[['amount']])

    anomalies = df[df['flag'] == -1]

    for _, r in anomalies.iterrows():
        engine.execute(f"""
            INSERT INTO risk_flags(user_id, date, flag_type, severity, message)
            VALUES ('{user_id}', '{r.ds}', 'ANOMALY_SPEND', 3,
            'Unusual spending detected')
        """)

from analytics.db import engine

def run_behavior_scan():
    rows = engine.execute("SELECT user_id, creep_ratio FROM lifestyle_creep").fetchall()
    for u, ratio in rows:
        if ratio and ratio > 1.2:
            engine.execute(f"""
              INSERT INTO behavior_flags(user_id,date,flag_type,severity,message)
              VALUES ('{u}', CURRENT_DATE, 'LIFESTYLE_CREEP', 4,
                      'Your spending grew >20% compared to last month')
            """)

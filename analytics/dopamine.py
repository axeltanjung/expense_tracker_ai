from analytics.db import engine

def run_dopamine():
    for u,c,a in engine.execute("SELECT user_id,cnt,avg_amt FROM dopamine_spend"):
        engine.execute("""
          INSERT INTO behavior_flags(user_id,date,flag_type,severity,message)
          VALUES (%s,CURRENT_DATE,'DOPAMINE_SPEND',3,
                  'Many small purchases detected (possible reward-seeking)')
        """, (u,))

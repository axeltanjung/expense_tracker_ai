from analytics.db import engine

def flag_if_impulse(user_id, merchant, amount):
    # Heuristik: transaksi kecil berulang dalam 24 jam → impulse
    r = engine.execute("""
      SELECT COUNT(*) FROM transactions
      WHERE user_id=%s AND merchant=%s AND direction='out'
        AND datetime >= now() - interval '24 hour'
    """, (user_id, merchant)).scalar() or 0

    if r >= 2:
        engine.execute("""
          INSERT INTO delayed_purchases(user_id,merchant,amount)
          VALUES (%s,%s,%s)
        """, (user_id, merchant, amount))

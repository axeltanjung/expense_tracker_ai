from sqlalchemy import text

def recompute_spend(user_id, db):
    db.execute(text("REFRESH MATERIALIZED VIEW spend_7d"))
    db.execute(text("REFRESH MATERIALIZED VIEW spend_30d"))
    db.execute(text("REFRESH MATERIALIZED VIEW spend_90d"))
    db.commit()

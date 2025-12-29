from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import SessionLocal
from sqlalchemy import text
from schemas import SpendInsight
from pydantic import BaseModel

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/insights/spend", response_model=SpendInsight)
def spend(user_id: str, db: Session = Depends(get_db)):
    q = """
    SELECT
      (SELECT COALESCE(SUM(spend_7d),0) FROM spend_7d WHERE user_id=:uid),
      (SELECT COALESCE(SUM(spend),0) FROM spend_30d WHERE user_id=:uid),
      (SELECT COALESCE(SUM(spend_90d),0) FROM spend_90d WHERE user_id=:uid)
    """
    r = db.execute(text(q), {"uid": user_id}).fetchone()
    return SpendInsight(spend_7d=r[0], spend_30d=r[1], spend_90d=r[2])

@router.get("/insights/runway")
def runway(user_id: str, db: Session = Depends(get_db)):
    q = """
    SELECT net_30d FROM cash_velocity WHERE user_id=:uid
    """
    net = db.execute(q, {"uid": user_id}).scalar() or 0
    avg_daily_burn = abs(net) / 30
    runway_days = 999 if avg_daily_burn == 0 else int(1000000 / avg_daily_burn)
    return {"runway_days": runway_days}

@router.get("/insights/subscriptions")
def subs(db: Session = Depends(get_db)):
    q = "SELECT merchant, avg_amt, cnt FROM subscriptions_detect"
    return [dict(r) for r in db.execute(q).fetchall()]

@router.get("/insights/risk")
def risk(user_id: str, db: Session = Depends(get_db)):
    q = """
    SELECT date, flag_type, severity, message
    FROM risk_flags WHERE user_id=:uid ORDER BY date DESC
    """
    return [dict(r) for r in db.execute(text(q), {"uid": user_id}).fetchall()]

class WhatIfRequest(BaseModel):
    user_id: str
    extra_monthly_cost: float   # simulasi cicilan / sewa / lifestyle

@router.post("/insights/whatif")
def whatif(req: WhatIfRequest, db: Session = Depends(get_db)):
    q = """
    SELECT
      COALESCE(SUM(CASE WHEN direction='in' THEN amount ELSE -amount END),0)
      FROM transactions
      WHERE user_id=:uid AND datetime >= now() - interval '30 day'
    """
    net = db.execute(text(q), {"uid": req.user_id}).scalar() or 0

    projected_net = net - req.extra_monthly_cost

    daily_burn = abs(projected_net) / 30 if projected_net < 0 else 0
    runway = 999 if daily_burn == 0 else int(1000000 / daily_burn)

    risk = "SAFE" if projected_net >= 0 else "RISK"

    return {
        "current_net_30d": net,
        "projected_net_30d": projected_net,
        "runway_days": runway,
        "risk": risk
    }

class ScenarioReq(BaseModel):
    user_id: str
    name: str
    extra_monthly_cost: float

@router.post("/insights/scenario")
def save_scenario(req: ScenarioReq, db: Session = Depends(get_db)):
    db.execute(text("""
        INSERT INTO scenarios(user_id,name,extra_monthly_cost)
        VALUES (:u,:n,:c)
    """), {"u":req.user_id,"n":req.name,"c":req.extra_monthly_cost})
    db.commit()
    return {"status":"saved"}

@router.get("/insights/scenario")
def list_scenarios(user_id: str, db: Session = Depends(get_db)):
    return db.execute(text("""
        SELECT id,name,extra_monthly_cost FROM scenarios
        WHERE user_id=:u ORDER BY id DESC
    """), {"u":user_id}).fetchall()

@router.get("/insights/fire")
def fire(user_id: str, target: float = 1000000000, db: Session = Depends(get_db)):
    net = db.execute(text("""
      SELECT COALESCE(SUM(CASE WHEN direction='in' THEN amount ELSE -amount END),0)
      FROM transactions WHERE user_id=:u AND datetime >= now()-interval '30 day'
    """), {"u":user_id}).scalar() or 0

    monthly_saving = max(net, 0)
    months = 999 if monthly_saving==0 else int(target/monthly_saving)
    return {"months_to_fire": months}

@router.post("/insights/goal_conflict")
def conflict(user_id: str, new_monthly_cost: float, db: Session = Depends(get_db)):
    net = db.execute(text("""
      SELECT COALESCE(SUM(CASE WHEN direction='in' THEN amount ELSE -amount END),0)
      FROM transactions WHERE user_id=:u AND datetime >= now()-interval '30 day'
    """), {"u":user_id}).scalar() or 0

    return {
      "can_afford": net - new_monthly_cost >= 0,
      "fire_delay_months": 0 if net<=0 else int((new_monthly_cost/net)*12)
    }

@router.get("/insights/behavior")
def behavior(user_id: str, db: Session = Depends(get_db)):
    return db.execute(text("""
      SELECT date,flag_type,severity,message
      FROM behavior_flags WHERE user_id=:u ORDER BY date DESC
    """), {"u":user_id}).fetchall()

@router.get("/insights/delayed")
def delayed(user_id: str, db: Session = Depends(get_db)):
    return db.execute(text("""
      SELECT id,merchant,amount,created_at,status
      FROM delayed_purchases WHERE user_id=:u AND status='PENDING'
      ORDER BY created_at DESC
    """), {"u":user_id}).fetchall()

@router.post("/insights/delayed/confirm")
def confirm(id:int, db: Session = Depends(get_db)):
    db.execute(text("UPDATE delayed_purchases SET status='CONFIRMED' WHERE id=:i"), {"i":id})
    db.commit()
    return {"ok":True}

@router.post("/insights/regret")
def regret(user_id:str, txn_id:str, db:Session=Depends(get_db)):
    db.execute(text("INSERT INTO regret_events(user_id,txn_id) VALUES (:u,:t)"),
               {"u":user_id,"t":txn_id})
    db.commit()
    return {"ok":True}

@router.get("/insights/regret")
def regret_stats(user_id:str, db:Session=Depends(get_db)):
    return db.execute(text("""
      SELECT t.merchant, COUNT(*) cnt
      FROM regret_events r JOIN transactions t ON r.txn_id=t.txn_id
      WHERE r.user_id=:u GROUP BY t.merchant ORDER BY cnt DESC
    """), {"u":user_id}).fetchall()

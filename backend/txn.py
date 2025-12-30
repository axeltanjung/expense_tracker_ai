from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from backend.db import get_db
from backend.ocr import extract_amount_and_merchant
from backend.recompute import spends, risk, fire, behavior
from backend.ml.category import predict_category
from pydantic import BaseModel

router = APIRouter()

class TxnReq(BaseModel):
    user_id: str
    amount: float
    merchant: str
    direction: str = "out"

@router.post("/txn")
def add_txn(txn: TxnReq, db: Session = Depends(get_db)):

    db.execute(text("""
      INSERT INTO transactions(txn_id,user_id,datetime,amount,direction,merchant)
      VALUES (gen_random_uuid(),:u,now(),:a,:d,:m)
    """), {
        "u": txn.user_id,
        "a": txn.amount,
        "d": txn.direction,
        "m": txn.merchant
    })
    db.commit()

    # AUTO-AI PIPELINE
    spends.recompute(txn.user_id, db)
    risk.recompute(txn.user_id, db)
    fire.recompute(txn.user_id, db)
    behavior.recompute(txn.user_id, db)

    return {"status": "ok"}

@router.post("/txn/ocr")
def ocr_receipt(file: UploadFile = File(...)):
    return extract_amount_and_merchant(file)

@router.get("/txn/predict_category")
def category(merchant: str):
    return predict_category(merchant)

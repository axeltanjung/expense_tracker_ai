from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from insights import router as insights_router
from pydantic import BaseModel
from db import SessionLocal
from sqlalchemy import text
from fastapi import UploadFile, File
from ocr import extract_amount_and_merchant
import joblib

app = FastAPI(title="Expense AI Engine")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Intelligence Routes
app.include_router(insights_router)

# Health check
@app.get("/")
def health():
    return {"status": "Expense AI Engine running"}

class TxnReq(BaseModel):
    user_id: str
    amount: float
    merchant: str
    direction: str = "out"

@app.post("/txn")
def add_txn(req: TxnReq):
    db = SessionLocal()
    db.execute(text("""
      INSERT INTO transactions(txn_id,user_id,datetime,amount,direction,merchant)
      VALUES (gen_random_uuid(),:u,now(),:a,:d,:m)
    """), {"u":req.user_id,"a":req.amount,"d":req.direction,"m":req.merchant})
    db.commit()
    db.close()
    return {"status":"ok"}

@app.post("/txn/ocr")
def upload_receipt(file: UploadFile = File(...)):
    path = f"/tmp/{file.filename}"
    with open(path, "wb") as f:
        f.write(file.file.read())
    return extract_amount_and_merchant(path)

model, vectorizer = joblib.load("models/category.pkl")

@app.get("/txn/predict_category")
def predict(merchant:str):
    return {"category": model.predict(vectorizer.transform([merchant]))[0]}
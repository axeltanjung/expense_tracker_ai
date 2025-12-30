from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.insights import router as insights_router
from backend.txn import router as txn_router

app = FastAPI(title="Expense AI Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(insights_router)
app.include_router(txn_router)

@app.get("/")
def health():
    return {"status": "ok"}

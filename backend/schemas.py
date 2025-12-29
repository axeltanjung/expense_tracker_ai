from pydantic import BaseModel

class SpendInsight(BaseModel):
    spend_7d: float
    spend_30d: float
    spend_90d: float

class SubscriptionLeak(BaseModel):
    merchant: str
    avg_amt: float
    cnt: int

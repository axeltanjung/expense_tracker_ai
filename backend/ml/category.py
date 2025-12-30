import os
import numpy as np
import joblib
from functools import lru_cache

MODEL_PATH = os.getenv("CATEGORY_MODEL_PATH", "models/category_clf.joblib")
DISABLE_ML = os.getenv("DISABLE_ML", "0") == "1"


@lru_cache
def get_model():
    if DISABLE_ML:
        return None
    return joblib.load(MODEL_PATH)


def _preprocess(amount: float, merchant: str):
    """
    Minimal deterministic feature builder.
    Bisa kamu upgrade ke TF-IDF / embedding kapanpun.
    """
    merchant = (merchant or "").lower()

    has_food_kw = any(k in merchant for k in ["cafe", "coffee", "bakery", "restaurant", "food"])
    has_transport_kw = any(k in merchant for k in ["uber", "grab", "gojek", "taxi", "train", "bus"])
    has_market_kw = any(k in merchant for k in ["mart", "market", "indomaret", "alfamart"])

    return np.array([[
        amount or 0.0,
        int(has_food_kw),
        int(has_transport_kw),
        int(has_market_kw),
        len(merchant)
    ]], dtype=float)


def predict_category(amount: float, merchant: str):
    """
    Deterministic category prediction.
    Returns (category, confidence)
    """

    if DISABLE_ML:
        return "unknown", 0.0

    model = get_model()
    X = _preprocess(amount, merchant)

    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(X)[0]
        idx = int(np.argmax(probs))
        return model.classes_[idx], float(probs[idx])
    else:
        return model.predict(X)[0], None

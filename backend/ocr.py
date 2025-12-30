from functools import lru_cache
import os
import re


DISABLE_OCR = os.getenv("DISABLE_OCR", "0") == "1"


@lru_cache
def get_ocr():
    from paddleocr import PaddleOCR   # lazy import
    return PaddleOCR(use_angle_cls=True, lang="en")


def extract_amount_and_merchant(image_path: str):
    if DISABLE_OCR:
        return {"merchant": None, "amount": None}

    ocr = get_ocr()
    res = ocr.ocr(image_path, cls=True)

    if not res or not res[0]:
        return {"merchant": None, "amount": None}

    text = " ".join([l[1][0] for l in res[0]])

    amt = re.findall(r"\d{1,3}(?:[.,]\d{3})+", text)

    return {
        "merchant": text[:40],
        "amount": float(amt[0].replace(",", "")) if amt else None
    }

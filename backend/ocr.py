from paddleocr import PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')

def extract_amount_and_merchant(image_path):
    res = ocr.ocr(image_path, cls=True)
    text = " ".join([l[1][0] for l in res[0]])

    import re
    amt = re.findall(r'\d{1,3}(?:[.,]\d{3})+', text)
    return {
        "merchant": text[:30],
        "amount": float(amt[0].replace(",", "")) if amt else None
    }

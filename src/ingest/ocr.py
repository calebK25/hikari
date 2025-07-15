from pdf2image import convert_from_path
import pytesseract, hashlib, json

def ocr_pdf(path: str):
    pages = convert_from_path(path, dpi=300)
    out = []
    for i, img in enumerate(pages, 1):
        text = pytesseract.image_to_string(img)
        sha = hashlib.sha256(text.encode()).hexdigest()[:8]
        out.append({"page": i, "text": text, "sha": sha})
    return out
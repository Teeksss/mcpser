from fastapi import FastAPI, UploadFile, File
from ocr_pdf_processor import extract_text_from_image, extract_text_from_pdf
import os

app = FastAPI()

@app.post("/process-image/")
async def process_image(file: UploadFile = File(...)):
    """
    Görüntü dosyasını alır ve OCR ile metni çıkarır.
    """
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    text = extract_text_from_image(file_path)
    os.remove(file_path)
    return {"text": text}

@app.post("/process-pdf/")
async def process_pdf(file: UploadFile = File(...)):
    """
    PDF dosyasını alır ve metni çıkarır.
    """
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    text = extract_text_from_pdf(file_path)
    os.remove(file_path)
    return {"text": text}
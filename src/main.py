from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import os
from PIL import Image
import pytesseract
from PyPDF2 import PdfReader

from src.api.v1.endpoints import (
    auth,
    user_admin,
    pipeline,
    metrics,
    tenant,
    vector,
    audit,
)
from src.services.logger import app_logger

app = FastAPI(
    title="MCP Server",
    description="Kurumsal Multi-Model RAG + LLM ve Vector Search Platformu",
    version="1.0.0",
)

# Rate Limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def ratelimit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(status_code=429, content={"detail": "Rate limit aşıldı."})

# Genel HTTP log middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    app_logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    app_logger.info(f"Response: {response.status_code} {request.method} {request.url}")
    return response

# OCR İşlevi
def extract_text_from_image(image_path):
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        return f"Error processing image: {e}"

# PDF İşleme İşlevi
def extract_text_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error processing PDF: {e}"

# OCR Endpoint
@app.post("/api/v1/ocr/image")
async def process_image(file: UploadFile = File(...)):
    """
    Görüntü dosyasını alır ve OCR ile metni çıkarır.
    """
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    try:
        text = extract_text_from_image(file_path)
    finally:
        os.remove(file_path)
    return {"text": text}

# PDF İşleme Endpoint
@app.post("/api/v1/ocr/pdf")
async def process_pdf(file: UploadFile = File(...)):
    """
    PDF dosyasını alır ve metni çıkarır.
    """
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    try:
        text = extract_text_from_pdf(file_path)
    finally:
        os.remove(file_path)
    return {"text": text}

# API Router kayıtları
app.include_router(auth.router)
app.include_router(user_admin.router)
app.include_router(pipeline.router)
app.include_router(metrics.router)
app.include_router(tenant.router)
app.include_router(vector.router)
app.include_router(audit.router)

@app.get("/api/v1/ping")
@limiter.limit("10/minute")
def ping():
    return {"status": "ok"}
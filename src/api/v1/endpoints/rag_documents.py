from fastapi import APIRouter, UploadFile, Form, File
from src.services.rag.rag_service import RAGService

router = APIRouter(prefix="/api/v1/rag", tags=["RAG"])

@router.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    ocr_lang: str = Form("eng+tur"),
):
    """
    OCR ve PDF işleme ile dosyaları RAG vektör mağazasına ekler.
    """
    rag = RAGService()
    result = await rag.ingest_file(file, ocr_lang)
    return result
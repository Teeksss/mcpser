from fastapi import APIRouter, Depends
from src.core.rbac import require_permission

router = APIRouter(prefix="/api/v1/pipeline", tags=["Pipeline"])

@router.post("/rag-inference", dependencies=[Depends(require_permission("use_llm"))])
def rag_inference(req: dict):
    # Burada model inference işlemleri yürütülür
    return {"result": "inference_result"}
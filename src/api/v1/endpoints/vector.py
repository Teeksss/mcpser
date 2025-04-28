from fastapi import APIRouter, Request
from src.core.tenant_context import get_tenant_id
from src.services.vector_store import VectorStoreManager

router = APIRouter(prefix="/api/v1/vector", tags=["Vector"])
vector_mgr = VectorStoreManager()

@router.post("/add")
def add_vector(request: Request, vector: list, metadata: dict):
    tenant_id = get_tenant_id(request)
    vector_mgr.add_vector(tenant_id, metadata, vector)
    return {"status": "ok"}

@router.post("/add_bulk")
def add_vectors_bulk(request: Request, vectors: list, metadatas: list):
    tenant_id = get_tenant_id(request)
    vector_mgr.add_vectors_bulk(tenant_id, vectors, metadatas)
    return {"status": "ok"}

@router.post("/query")
def query_vector(request: Request, query: str, filter: dict = None):
    tenant_id = get_tenant_id(request)
    results = vector_mgr.query(tenant_id, query, filter)
    return {"results": results}

@router.post("/delete")
def delete_by_metadata(request: Request, filter: dict):
    tenant_id = get_tenant_id(request)
    vector_mgr.delete_by_metadata(tenant_id, filter)
    return {"status": "deleted"}
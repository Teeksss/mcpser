from fastapi import APIRouter, Depends
from src.core.rbac import require_permission

router = APIRouter(prefix="/api/v1/audit", tags=["Audit"])

@router.get("/", dependencies=[Depends(require_permission("admin"))])
def get_audit_logs():
    with open("./logs/audit.log", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines()]
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.models.database import SessionLocal
from src.models.tenant import Tenant
from src.core.rbac import require_permission

router = APIRouter(prefix="/api/v1/tenants", tags=["Tenants"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", dependencies=[Depends(require_permission("admin"))])
def list_tenants(db: Session = Depends(get_db)):
    return db.query(Tenant).all()

@router.post("/", dependencies=[Depends(require_permission("admin"))])
def create_tenant(name: str, description: str = "", db: Session = Depends(get_db)):
    if db.query(Tenant).filter(Tenant.name == name).first():
        raise HTTPException(status_code=409, detail="Tenant mevcut")
    tenant = Tenant(name=name, description=description)
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant
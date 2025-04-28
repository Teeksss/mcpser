from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.models.database import SessionLocal
from src.models.user import User
from src.core.rbac import require_permission
from src.services.audit_log import audit_logger

router = APIRouter(prefix="/api/v1/users", tags=["Users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", dependencies=[Depends(require_permission("admin"))])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.post("/{user_id}/role", dependencies=[Depends(require_permission("admin"))])
def update_role(user_id: int, role: str, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı yok")
    old_role = user.role
    user.role = role
    db.commit()
    audit_logger.log(user.username, "role_update", f"{old_role}→{role}")
    return {"status": "ok", "user_id": user.id, "role": role}
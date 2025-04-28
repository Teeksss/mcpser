from fastapi import APIRouter, HTTPException, Depends, Body
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.core.security import (
    verify_password, get_password_hash, create_access_token,
    create_refresh_token, decode_token
)
from src.models.database import SessionLocal
from src.models.user import User
from src.core.rbac import get_current_user
from datetime import timedelta
from src.services.audit_log import audit_logger

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str
    email: str = None

class TokenOut(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login", response_model=TokenOut)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user: User = db.query(User).filter(User.username == req.username).first()
    if not user or not verify_password(req.password, user.hashed_password):
        audit_logger.log(req.username, "login_failed", "wrong password or user not found")
        raise HTTPException(status_code=401, detail="Kullanıcı adı veya şifre hatalı")
    token_data = {"sub": user.username, "role": user.role}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    audit_logger.log(user.username, "login_success")
    return TokenOut(access_token=access_token, refresh_token=refresh_token)

@router.post("/register")
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == req.username).first():
        raise HTTPException(status_code=409, detail="Kullanıcı adı mevcut")
    user = User(
        username=req.username,
        hashed_password=get_password_hash(req.password),
        email=req.email,
        role="user"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    audit_logger.log(user.username, "register")
    return {"status": "success", "user_id": user.id}

@router.post("/refresh", response_model=TokenOut)
def refresh_token(refresh_token: str = Body(...)):
    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Geçersiz refresh token")
    token_data = {k: payload[k] for k in ("sub", "role")}
    access_token = create_access_token(token_data)
    new_refresh_token = create_refresh_token(token_data)
    return TokenOut(access_token=access_token, refresh_token=new_refresh_token)

@router.get("/me")
def me(user=Depends(get_current_user)):
    return user
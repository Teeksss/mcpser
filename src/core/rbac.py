from fastapi import HTTPException, Header, Depends
from src.core.security import decode_token

ROLE_PERMISSIONS = {
    "admin": ["all"],
    "user": [
        "upload_document",
        "view_documents",
        "use_llm"
    ]
}

def get_current_user(token: str = Header(..., alias="Authorization")):
    if token.startswith("Bearer "):
        token = token[7:]
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Geçersiz veya süresi dolmuş token")
    return payload

def require_permission(permission: str):
    def checker(user=Depends(get_current_user)):
        role = user.get("role")
        allowed = ROLE_PERMISSIONS.get(role, [])
        if "all" in allowed or permission in allowed:
            return user
        raise HTTPException(status_code=403, detail="Yetkisiz")
    return checker
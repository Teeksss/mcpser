from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

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
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from api.auth import router as auth_router
from api.project import router as project_router
from api.api_key import router as api_key_router
from api.prompt_scan import router as prompt_scan_router
from api.dashboard import router as dashboard_router
from api.threat_log import router as threat_log_router
from api.firewall import router as firewall_router
from api.firewall_rule import router as firewall_rule_router

from database.connection import engine, Base
from database.models.user import User
from database.models.project import Project
from database.models.api_key import APIKey
from database.models.threat_log import ThreatLog
from database.models.firewall_rule import FirewallRule

from core.config import settings
from core.rate_limit import RateLimitMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="SecureShield AI",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if settings.ENVIRONMENT == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.CORS_ORIGINS + ["localhost", "127.0.0.1"],
    )

app.add_middleware(RateLimitMiddleware, max_requests=60, window_seconds=60)

app.include_router(auth_router)
app.include_router(project_router)
app.include_router(api_key_router)
app.include_router(prompt_scan_router)
app.include_router(dashboard_router)
app.include_router(threat_log_router)
app.include_router(firewall_router)
app.include_router(firewall_rule_router)


@app.get("/")
def home():
    return {
        "message": "SecureShield AI Backend Running",
        "version": "1.0.0"
    }

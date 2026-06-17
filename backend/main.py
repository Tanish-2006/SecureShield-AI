
from contextlib import asynccontextmanager

from fastapi import FastAPI
from api.auth import router as auth_router
from api.project import router as project_router
from database.connection import engine, Base
from database.models.firewall_rule import FirewallRule
from database.models.api_key import APIKey
from api.api_key import router as api_key_router
from api.prompt_scan import router as prompt_scan_router
from database.models.user import User
from api.firewall import router as firewall_router
from database.models.threat_log import ThreatLog
from api.dashboard import router as dashboard_router
from database.models.project import Project
from api.threat_log import (
    router as threat_log_router
)

from api.firewall_rule import (
    router as firewall_rule_router
)

from fastapi.middleware.cors import CORSMiddleware
from core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="SecureShield AI",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        "message": "SecureShield AI Backend Running"
    }

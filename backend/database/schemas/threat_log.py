from datetime import datetime

from pydantic import BaseModel


class ThreatLogResponse(BaseModel):
    id: int
    project_id: int | None = None
    severity: str
    threats: str
    risk_score: int
    action: str
    prompt: str
    created_at: datetime

    class Config:
        from_attributes = True

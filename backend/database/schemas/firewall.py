from pydantic import BaseModel, Field


class FirewallRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=10000)
    project_id: int


class FirewallResponse(BaseModel):
    risk_score: int
    severity: str
    decision: str
    reason: str

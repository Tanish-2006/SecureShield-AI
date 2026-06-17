from pydantic import BaseModel, Field


class PromptScanRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=10000)
    project_id: int


class PromptScanResponse(BaseModel):
    risk_score: int
    severity: str
    threats: list[str]
    action: str
    confidence: float

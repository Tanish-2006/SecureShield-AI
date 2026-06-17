from pydantic import BaseModel, Field


class FirewallRuleCreate(BaseModel):
    project_id: int
    risk_threshold: int = Field(ge=1, le=100)


class FirewallRuleResponse(BaseModel):
    id: int
    project_id: int
    risk_threshold: int

    class Config:
        from_attributes = True

from datetime import datetime

from pydantic import BaseModel, Field


class APIKeyCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    provider: str = Field(min_length=2, max_length=80)
    api_key: str = Field(min_length=8, max_length=500)
    project_id: int


class APIKeyResponse(BaseModel):
    id: int
    name: str
    provider: str
    project_id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

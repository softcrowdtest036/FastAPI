from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class JobPositionBase(BaseModel):
    title: str
    description: str
    min_salary: float
    max_salary: float
    branch_name: str
    job_type: str
    status: str = Field(default="active", regex="^(active|inactive)$")
    image_url: Optional[str] = None

class JobPositionCreate(JobPositionBase):
    pass

class JobPositionResponse(JobPositionBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

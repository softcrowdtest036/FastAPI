from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class JobPositionBase(BaseModel):
    title: str
    description: str
    min_salary: float
    max_salary: float
    branch_name: str 
    job_type: str
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

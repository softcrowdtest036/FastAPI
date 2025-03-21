from pydantic import BaseModel, Field
from datetime import datetime

class CategoryModel(BaseModel):
    id: str = Field(..., alias="_id")  # Convert MongoDB _id to id
    name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True  # Ensures alias `_id` is respected
        from_attributes = True
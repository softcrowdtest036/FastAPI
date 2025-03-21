# app/schemas/gallery_cat.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class GalleryCreate(BaseModel):
    """Schema for creating a gallery category."""
    name: str

class GalleryCategoryUpdate(BaseModel):
    """Schema for updating a gallery category."""
    name: Optional[str] = None

class GalleryCategoryResponse(BaseModel):
    """Schema for responding with a gallery category."""
    id: str
    name: str
    created_at: datetime

    class Config:
        from_attributes = True  # Updated from orm_mode
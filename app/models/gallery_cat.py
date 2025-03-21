# app/models/gallery_cat.py
from pydantic import BaseModel
from datetime import datetime

class GalleryModel(BaseModel):
    """Base model for gallery categories."""
    name: str
    created_at: datetime = datetime.utcnow()
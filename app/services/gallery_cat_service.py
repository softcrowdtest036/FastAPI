# app/services/gallery_cat_service.py
from typing import List, Optional
from bson import ObjectId
from fastapi import HTTPException
from app.core.database import mongodb
from app.schemas.gallery_cat import GalleryCategoryResponse  # Correct import
from datetime import datetime

async def create_gallery_category(category_data: dict) -> GalleryCategoryResponse:
    """Create a new gallery category."""
    category_data["created_at"] = datetime.utcnow()
    result = await mongodb.get_database().gallery_categories.insert_one(category_data)
    inserted_category = await mongodb.get_database().gallery_categories.find_one({"_id": result.inserted_id})

    if inserted_category:
        inserted_category["id"] = str(inserted_category.pop("_id"))  # Convert _id to id
        return GalleryCategoryResponse(**inserted_category)
    raise HTTPException(status_code=500, detail="Failed to create gallery category")

async def get_gallery_category(category_id: str) -> Optional[GalleryCategoryResponse]:
    """Retrieve a gallery category by ID."""
    category = await mongodb.get_database().gallery_categories.find_one({"_id": ObjectId(category_id)})
    if category:
        category["id"] = str(category.pop("_id"))  # Convert _id to id
        return GalleryCategoryResponse(**category)
    return None

async def get_all_gallery_categories() -> List[GalleryCategoryResponse]:
    """Retrieve all gallery categories."""
    categories = await mongodb.get_database().gallery_categories.find().to_list(None)
    for category in categories:
        category["id"] = str(category.pop("_id"))  # Convert _id to id
    return [GalleryCategoryResponse(**category) for category in categories]

async def update_gallery_category(category_id: str, category_data: dict) -> Optional[GalleryCategoryResponse]:
    """Update a gallery category by ID."""
    await mongodb.get_database().gallery_categories.update_one({"_id": ObjectId(category_id)}, {"$set": category_data})
    updated_category = await get_gallery_category(category_id)
    return updated_category

async def delete_gallery_category(category_id: str) -> bool:
    """Delete a gallery category by ID."""
    result = await mongodb.get_database().gallery_categories.delete_one({"_id": ObjectId(category_id)})
    return result.deleted_count > 0
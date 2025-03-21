from typing import Optional, List
from bson import ObjectId
from app.core.database import mongodb
from app.models.categories import CategoryModel

async def create_category(category_data: dict) -> CategoryModel:
    """Create a new category."""
    result = await mongodb.get_database().categories.insert_one(category_data)
    
    # Fetch the inserted document and ensure `_id` is converted to `id`
    inserted_category = await mongodb.get_database().categories.find_one({"_id": result.inserted_id})
    
    if inserted_category:
        inserted_category["id"] = str(inserted_category.pop("_id"))  # Convert _id to id
    
    return CategoryModel(**inserted_category)

async def get_category(category_id: str) -> Optional[CategoryModel]:
    """Retrieve a category by ID."""
    category = await mongodb.get_database().categories.find_one({"_id": ObjectId(category_id)})
    if category:
        category["id"] = str(category.pop("_id"))  # Convert _id to id
        return CategoryModel(**category)

async def get_all_categories() -> List[CategoryModel]:
    """Retrieve all categories."""
    categories = await mongodb.get_database().categories.find().to_list(None)
    
    for category in categories:
        category["id"] = str(category.pop("_id"))  # Convert _id to id
    
    return [CategoryModel(**category) for category in categories]

async def update_category(category_id: str, category_data: dict) -> Optional[CategoryModel]:
    """Update a category."""
    await mongodb.get_database().categories.update_one({"_id": ObjectId(category_id)}, {"$set": category_data})
    
    updated_category = await get_category(category_id)
    
    if updated_category:
        return updated_category

async def delete_category(category_id: str) -> bool:
    """Delete a category."""
    result = await mongodb.get_database().categories.delete_one({"_id": ObjectId(category_id)})
    return result.deleted_count > 0
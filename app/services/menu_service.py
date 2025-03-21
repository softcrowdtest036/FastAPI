import os
from typing import List, Optional
from bson import ObjectId
from fastapi import UploadFile, HTTPException
from app.core.database import mongodb
from app.models.menu import MenuModel
from datetime import datetime

# Ensure the static/images directory exists
os.makedirs("static/images", exist_ok=True)

async def save_image(file: UploadFile) -> str:
    """Save an uploaded image to the static/images folder and return the file path."""
    file_path = f"static/images/{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    return f"/static/images/{file.filename}"

async def create_menu_item(menu_data: dict, image: Optional[UploadFile] = None) -> MenuModel:
    """Create a new menu item."""
    # Check if category exists
    category_exists = await mongodb.get_database().categories.find_one(
        {"name": menu_data["category_name"]}
    )
    if not category_exists:
        raise HTTPException(status_code=400, detail="Category does not exist")

    if image:
        image_url = await save_image(image)
        menu_data["image_url"] = image_url

    result = await mongodb.get_database().menu.insert_one(menu_data)
    inserted_item = await mongodb.get_database().menu.find_one({"_id": result.inserted_id})

    if inserted_item:
        inserted_item["id"] = str(inserted_item.pop("_id"))  # Convert _id to id
        return MenuModel(**inserted_item)
    raise HTTPException(status_code=500, detail="Failed to create menu item")

async def get_menu_item(menu_id: str) -> Optional[MenuModel]:
    """Retrieve a menu item by ID."""
    item = await mongodb.get_database().menu.find_one({"_id": ObjectId(menu_id)})
    if item:
        item["id"] = str(item.pop("_id"))  # Convert _id to id
        return MenuModel(**item)
    return None

async def get_all_menu_items() -> List[MenuModel]:
    """Retrieve all menu items."""
    items = await mongodb.get_database().menu.find().to_list(None)
    for item in items:
        item["id"] = str(item.pop("_id"))  # Convert _id to id
    return [MenuModel(**item) for item in items]

async def get_menu_items_by_category(category_name: str) -> List[MenuModel]:
    """Retrieve menu items by category name."""
    items = await mongodb.get_database().menu.find({"category_name": category_name}).to_list(None)
    for item in items:
        item["id"] = str(item.pop("_id"))  # Convert _id to id
    return [MenuModel(**item) for item in items]

async def update_menu_item(menu_id: str, menu_data: dict, image: Optional[UploadFile] = None) -> Optional[MenuModel]:
    """Update a menu item."""
    # Check if category exists (if provided in update)
    if "category_name" in menu_data and menu_data["category_name"]:
        category_exists = await mongodb.get_database().categories.find_one(
            {"name": menu_data["category_name"]}
        )
        if not category_exists:
            raise HTTPException(status_code=400, detail="Category does not exist")

    if image:
        image_url = await save_image(image)
        menu_data["image_url"] = image_url

    await mongodb.get_database().menu.update_one({"_id": ObjectId(menu_id)}, {"$set": menu_data})
    updated_item = await get_menu_item(menu_id)
    return updated_item

async def delete_menu_item(menu_id: str) -> bool:
    """Delete a menu item."""
    result = await mongodb.get_database().menu.delete_one({"_id": ObjectId(menu_id)})
    return result.deleted_count > 0
import os
from typing import Optional
from fastapi import UploadFile
from bson import ObjectId
from app.core.database import mongodb
from app.models.branches import BranchModel

# Ensure static/images directory exists
os.makedirs("static/images", exist_ok=True)

async def save_image(file: UploadFile) -> str:
    """Save an uploaded image and return the file path."""
    file_path = f"static/images/{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    return f"/{file_path}"

async def create_branch(branch_data: dict, image: Optional[UploadFile] = None) -> BranchModel:
    """Create a new branch with an optional image."""
    if image:
        branch_data["image_url"] = await save_image(image)

    # Insert into MongoDB
    result = await mongodb.get_database().branches.insert_one(branch_data)
    
    # Retrieve the inserted document and ensure `_id` is converted to `id`
    inserted_branch = await mongodb.get_database().branches.find_one({"_id": result.inserted_id})
    
    if inserted_branch:
        inserted_branch["id"] = str(inserted_branch.pop("_id"))  # Convert _id to id
    
    return BranchModel(**inserted_branch)

async def get_branch(branch_id: str) -> Optional[BranchModel]:
    """Retrieve a branch by ID."""
    branch = await mongodb.get_database().branches.find_one({"_id": ObjectId(branch_id)})
    if branch:
        branch["id"] = str(branch.pop("_id"))  # Convert _id to id
        return BranchModel(**branch)

async def get_all_branches() -> list[BranchModel]:
    """Retrieve all branches."""
    branches = await mongodb.get_database().branches.find().to_list(None)
    
    for branch in branches:
        branch["id"] = str(branch.pop("_id"))  # Convert _id to id
    
    return [BranchModel(**branch) for branch in branches]

async def update_branch(branch_id: str, branch_data: dict, image: Optional[UploadFile] = None) -> Optional[BranchModel]:
    """Update a branch."""
    if image:
        branch_data["image_url"] = await save_image(image)

    await mongodb.get_database().branches.update_one({"_id": ObjectId(branch_id)}, {"$set": branch_data})
    
    updated_branch = await get_branch(branch_id)
    
    if updated_branch:
        return updated_branch

async def delete_branch(branch_id: str) -> bool:
    """Delete a branch."""
    result = await mongodb.get_database().branches.delete_one({"_id": ObjectId(branch_id)})
    return result.deleted_count > 0
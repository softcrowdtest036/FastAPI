from typing import List, Optional
from bson import ObjectId
from fastapi import HTTPException, UploadFile
from app.core.database import mongodb
from app.schemas.image import ImageResponse
from datetime import datetime
import os

async def create_image(image_data: dict, file: UploadFile) -> ImageResponse:
    """Create a new image."""
    # Save the file to the static/images directory
    file_path = f"static/images/{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    image_data["file_path"] = file_path
    image_data["created_at"] = datetime.utcnow()
    
    # Ensure categoryId is stored as a string (if necessary)
    if "category_id" in image_data:
        image_data["categoryId"] = str(image_data["category_id"])
    
    result = await mongodb.get_database().images.insert_one(image_data)
    inserted_image = await mongodb.get_database().images.find_one({"_id": result.inserted_id})

    if inserted_image:
        inserted_image["id"] = str(inserted_image.pop("_id"))  # Convert _id to id
        return ImageResponse(**inserted_image)
    raise HTTPException(status_code=500, detail="Failed to create image")

async def get_image(image_id: str) -> Optional[ImageResponse]:
    """Retrieve an image by ID."""
    image = await mongodb.get_database().images.find_one({"_id": ObjectId(image_id)})
    if image:
        image["id"] = str(image.pop("_id"))  # Convert _id to id
        return ImageResponse(**image)
    return None

async def get_all_images() -> List[ImageResponse]:
    """Retrieve all images."""
    images = await mongodb.get_database().images.find().to_list(None)
    for image in images:
        image["id"] = str(image.pop("_id"))  # Convert _id to id
        if "categoryId" in image:
            image["categoryId"] = str(image["categoryId"])  # Ensure categoryId is a string
    return [ImageResponse(**image) for image in images]

async def update_image(image_id: str, image_data: dict, file: Optional[UploadFile] = None) -> Optional[ImageResponse]:
    """Update an image by ID."""
    if file:
        # Save the new file to the static/images directory
        file_path = f"static/images/{file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        image_data["file_path"] = file_path

    # Update the image in the database
    await mongodb.get_database().images.update_one({"_id": ObjectId(image_id)}, {"$set": image_data})
    updated_image = await get_image(image_id)
    return updated_image

async def delete_image(image_id: str) -> bool:
    """Delete an image by ID."""
    image = await get_image(image_id)
    if image:
        # Remove the file from the filesystem
        os.remove(image.file_path)
    result = await mongodb.get_database().images.delete_one({"_id": ObjectId(image_id)})
    return result.deleted_count > 0
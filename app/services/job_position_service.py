from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime
from fastapi import UploadFile
from typing import Optional
import os
from app.models.job_position import JobPositionCreate, JobPositionResponse

os.makedirs("static/images", exist_ok=True)

async def save_image(file: UploadFile) -> str:
    """Save an uploaded image and return the file path."""
    file_path = f"static/images/{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    return f"/{file_path}"

async def create_job_position(db: AsyncIOMotorDatabase, job_data: dict, image: Optional[UploadFile] = None) -> JobPositionResponse:
    """Create a new job position with an optional image."""
    if image:
        job_data["image_url"] = await save_image(image)
    
    # Add timestamps
    job_data["created_at"] = datetime.utcnow()
    job_data["updated_at"] = datetime.utcnow()
    
    # Insert into MongoDB
    result = await db.job_positions.insert_one(job_data)
    
    # Retrieve the inserted document and ensure `_id` is converted to `id`
    inserted_job = await db.job_positions.find_one({"_id": result.inserted_id})
    if inserted_job:
        inserted_job["id"] = str(inserted_job.pop("_id"))  # Convert _id to id
    
    return JobPositionResponse(**inserted_job)

async def get_all_job_positions(db: AsyncIOMotorDatabase):
    """Retrieve all job positions."""
    jobs = await db.job_positions.find().to_list(None)
    for job in jobs:
        job["id"] = str(job.pop("_id"))  # Convert _id to id
    return [JobPositionResponse(**job) for job in jobs]

async def get_job_position_by_id(db: AsyncIOMotorDatabase, job_id: str):
    """Retrieve a job position by ID."""
    job = await db.job_positions.find_one({"_id": ObjectId(job_id)})
    if job:
        job["id"] = str(job.pop("_id"))  # Convert _id to id
        return JobPositionResponse(**job)
    return None

async def update_job_position(db: AsyncIOMotorDatabase, job_id: str, job_data: dict, image: Optional[UploadFile] = None) -> Optional[JobPositionResponse]:
    """Update a job position with an optional image."""
    if image:
        job_data["image_url"] = await save_image(image)
    
    # Add updated_at timestamp
    job_data["updated_at"] = datetime.utcnow()
    
    # Update the job position in MongoDB
    result = await db.job_positions.update_one(
        {"_id": ObjectId(job_id)},
        {"$set": job_data}
    )
    
    if result.modified_count > 0:
        return await get_job_position_by_id(db, job_id)
    return None

async def delete_job_position(db: AsyncIOMotorDatabase, job_id: str):
    """Delete a job position."""
    result = await db.job_positions.delete_one({"_id": ObjectId(job_id)})
    return {"deleted": result.deleted_count}
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from app.core.database import mongodb
from app.models.job_position import JobPositionCreate, JobPositionResponse
from app.services.job_position_service import (
    create_job_position,
    get_all_job_positions,
    get_job_position_by_id,
    update_job_position,
    delete_job_position,
    save_image,
)

router = APIRouter()

async def get_database():
    """Ensure the database is connected before returning the database instance."""
    if mongodb.database is None:
        await mongodb.connect()
    return mongodb.get_database()

@router.post("/", response_model=JobPositionResponse)
async def add_job_position(
    title: str,
    description: str,
    min_salary: float,
    max_salary: float,
    branch_name: str,
    job_type: str,
    status: str = "active",  # Add status field with default value
    image: UploadFile = File(None),
    db=Depends(get_database)
):
    """API to create a job position."""
    job_data = {
        "title": title,
        "description": description,
        "min_salary": min_salary,
        "max_salary": max_salary,
        "branch_name": branch_name,
        "job_type": job_type,
        "status": status,  # Include status in job_data
        "image_url": None,
    }
    if image:
        job_data["image_url"] = await save_image(image)
    return await create_job_position(db, job_data)

@router.get("/", response_model=list[JobPositionResponse])
async def list_job_positions(db=Depends(get_database)):
    """API to get all job positions."""
    return await get_all_job_positions(db)

@router.get("/{job_id}", response_model=JobPositionResponse)
async def retrieve_job_position(job_id: str, db=Depends(get_database)):
    """API to get a job position by ID."""
    job = await get_job_position_by_id(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job position not found")
    return job

@router.put("/{job_id}", response_model=JobPositionResponse)
async def modify_job_position(
    job_id: str,
    title: str,
    description: str,
    min_salary: float,
    max_salary: float,
    branch_name: str,
    job_type: str,
    status: str,  # Add status field
    image: UploadFile = File(None),
    db=Depends(get_database)
):
    """API to update a job position with an optional image."""
    job_data = {
        "title": title,
        "description": description,
        "min_salary": min_salary,
        "max_salary": max_salary,
        "branch_name": branch_name,
        "job_type": job_type,
        "status": status,  # Include status in job_data
    }
    
    # Update the job position with the new data and optional image
    updated_job = await update_job_position(db, job_id, job_data, image)
    if not updated_job:
        raise HTTPException(status_code=404, detail="Job position not found or no changes made")
    return updated_job

@router.delete("/{job_id}")
async def remove_job_position(job_id: str, db=Depends(get_database)):
    """API to delete a job position."""
    return await delete_job_position(db, job_id)
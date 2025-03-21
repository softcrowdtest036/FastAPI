from fastapi import APIRouter, Depends
from app.core.database import mongodb
from app.schemas.career import JobApplicationCreate
from app.services.career_service import apply_for_job, get_all_applications, get_application_by_id, update_application_status
router = APIRouter()

async def get_database():
    """Ensure the database is connected before returning the database instance."""
    if not mongodb.database:
        await mongodb.connect()
    return mongodb.get_database()

@router.post("/apply", response_model=dict)
async def submit_job_application(application: JobApplicationCreate, db=Depends(get_database)):
    """Submit a job application."""
    return await apply_for_job(db, application)

@router.get("/applications", response_model=list)
async def list_all_applications(db=Depends(get_database)):
    """Fetch all job applications."""
    return await get_all_applications(db)

@router.get("/applications/{application_id}", response_model=dict)
async def get_application(application_id: str, db=Depends(get_database)):
    """Fetch a job application by its ID."""
    return await get_application_by_id(db, application_id)

@router.put("/applications/{application_id}/status", response_model=dict)
async def update_status(application_id: str, status: str, db=Depends(get_database)):
    """Update the status of a job application."""
    return await update_application_status(db, application_id, status)
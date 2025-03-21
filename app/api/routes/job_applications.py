from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from app.core.database import mongodb
from app.models.job_applications import JobApplicationCreate, JobApplicationResponse, ALLOWED_STATUSES
from app.services.job_applications_service import (
    create_job_application,
    get_all_job_applications,
    get_job_application_by_id,
    update_job_application_status,
    delete_job_application,
    filter_job_applications_by_title
)

router = APIRouter()

async def get_database():
    if mongodb.database is None:
        await mongodb.connect()
    return mongodb.get_database()

@router.post("/", response_model=JobApplicationResponse)
async def add_job_application(
    full_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    address: str = Form(None),
    job_position_id: str = Form(...),
    job_position_title: str = Form(...),
    experience: str = Form(None),
    skills: str = Form(None),
    cover_letter: str = Form(None),
    resume: UploadFile = File(None),
    db=Depends(get_database)
):
    data = JobApplicationCreate(
        full_name=full_name,
        email=email,
        phone=phone,
        address=address,
        job_position_id=job_position_id,
        job_position_title=job_position_title,
        experience=experience,
        skills=skills,
        cover_letter=cover_letter
    )
    return await create_job_application(db, data, resume)

@router.get("/", response_model=list[JobApplicationResponse])
async def list_job_applications(db=Depends(get_database)):
    """Get all job applications (no filters)"""
    return await get_all_job_applications(db)

@router.get("/filter", response_model=list[JobApplicationResponse])
async def filter_job_applications(job_title: str, db=Depends(get_database)):
    """Filter job applications by job title"""
    return await filter_job_applications_by_title(db, job_title)

@router.get("/{application_id}", response_model=JobApplicationResponse)
async def retrieve_job_application(application_id: str, db=Depends(get_database)):
    app = await get_job_application_by_id(db, application_id)
    if not app:
        raise HTTPException(status_code=404, detail="Job application not found")
    return app

@router.put("/{application_id}/status/{status}")
async def modify_job_application_status(application_id: str, status: str, db=Depends(get_database)):
    if status not in ALLOWED_STATUSES:
        raise HTTPException(status_code=400, detail=f"Invalid status. Allowed statuses: {ALLOWED_STATUSES}")
    return await update_job_application_status(db, application_id, status)

@router.delete("/{application_id}")
async def remove_job_application(application_id: str, db=Depends(get_database)):
    return await delete_job_application(db, application_id)

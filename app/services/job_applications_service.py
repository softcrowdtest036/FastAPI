from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime
from fastapi import UploadFile, HTTPException
import os
from typing import Optional
from app.utils.email import send_email
from app.models.job_applications import JobApplicationCreate, JobApplicationResponse, ALLOWED_STATUSES
from jinja2 import Environment, FileSystemLoader
# resume
os.makedirs("static/resumes", exist_ok=True)

env = Environment(loader=FileSystemLoader('app/templates/emails'))

async def save_resume(file: UploadFile) -> str:
    """Save uploaded resume and return file path."""
    file_path = f"static/resumes/{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    return f"/{file_path}"

async def create_job_application(
    db: AsyncIOMotorDatabase, application_data: JobApplicationCreate, resume: Optional[UploadFile] = None
) -> JobApplicationResponse:
    """Create a new job application."""
    data = application_data.dict()

    if resume:
        data["resume_url"] = await save_resume(resume)

    data["created_at"] = datetime.utcnow()
    data["updated_at"] = datetime.utcnow()

    result = await db.job_applications.insert_one(data)
    inserted = await db.job_applications.find_one({"_id": result.inserted_id})
    inserted["id"] = str(inserted.pop("_id"))

    subject = "Thank You for Applying!"
    template = env.get_template("application_confirmation.html")
    html_body = template.render(
        full_name=data['full_name'],
        job_position_title=data['job_position_title'],
        current_year=datetime.utcnow().year
    )
    send_email(data['email'], subject, html_body)

    return JobApplicationResponse(**inserted)

async def get_all_job_applications(db: AsyncIOMotorDatabase):
    """Get all job applications."""
    applications = await db.job_applications.find().to_list(None)
    for app in applications:
        app["id"] = str(app.pop("_id"))
    return [JobApplicationResponse(**app) for app in applications]

async def filter_job_applications_by_title(db: AsyncIOMotorDatabase, job_title: str):
    """Filter job applications by job title."""
    query = {"job_position_title": job_title}
    applications = await db.job_applications.find(query).to_list(None)
    for app in applications:
        app["id"] = str(app.pop("_id"))
    return [JobApplicationResponse(**app) for app in applications]

async def get_job_application_by_id(db: AsyncIOMotorDatabase, application_id: str):
    """Get job application by ID."""
    app = await db.job_applications.find_one({"_id": ObjectId(application_id)})
    if app:
        app["id"] = str(app.pop("_id"))
        return JobApplicationResponse(**app)
    return None

async def update_job_application_status(db: AsyncIOMotorDatabase, application_id: str, status: str):
    """Update status of job application."""
    if status not in ALLOWED_STATUSES:
        raise HTTPException(status_code=400, detail=f"Invalid status. Allowed statuses: {ALLOWED_STATUSES}")

    result = await db.job_applications.update_one(
        {"_id": ObjectId(application_id)},
        {"$set": {"status": status, "updated_at": datetime.utcnow()}}
    )
    app = await db.job_applications.find_one({"_id": ObjectId(application_id)})
    if app:
        subject = f"Application Status Updated: {status}"
        template = env.get_template("status_update.html")
        html_body = template.render(
            full_name=app.get('full_name'),
            job_position_title=app.get('job_position_title'),
            status=status,
            current_year=datetime.utcnow().year
        )
        send_email(app.get('email'), subject, html_body)

    return {"updated": result.modified_count}

async def delete_job_application(db: AsyncIOMotorDatabase, application_id: str):
    """Delete job application by ID."""
    result = await db.job_applications.delete_one({"_id": ObjectId(application_id)})
    return {"deleted": result.deleted_count}

# banjos_restaurant\app\services\career_service.py
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.schemas.career import JobApplicationCreate
from datetime import datetime
from bson import ObjectId
from app.utils.email import send_email
from app.models.career import job_application_helper

async def apply_for_job(db: AsyncIOMotorDatabase, application_data: JobApplicationCreate):
    application_dict = application_data.dict()
    application_dict["created_at"] = datetime.utcnow()
    application_dict["updated_at"] = datetime.utcnow()
    application_dict["application_status"] = "pending"

    result = await db.job_applications.insert_one(application_dict)
    application_dict["_id"] = str(result.inserted_id)

    subject = "Job Application Submitted Successfully"
    body = f"""
    Hello {application_data.applicant_name},

    Your application for the {application_data.job_title} position has been successfully received.
    Our HR team will review your application and get back to you soon.

    Regards,
    Banjo's Restaurant Team
    """
    send_email(application_data.applicant_email, subject, body)

    return application_dict

async def get_all_applications(db: AsyncIOMotorDatabase):
    applications = await db.job_applications.find().to_list(None)
    return [job_application_helper(app) for app in applications]

async def get_application_by_id(db: AsyncIOMotorDatabase, application_id: str):
    application = await db.job_applications.find_one({"_id": ObjectId(application_id)})
    return job_application_helper(application) if application else None

async def update_application_status(db: AsyncIOMotorDatabase, application_id: str, status: str):
    application = await db.job_applications.find_one({"_id": ObjectId(application_id)})
    if not application:
        return {"updated": 0}

    result = await db.job_applications.update_one(
        {"_id": ObjectId(application_id)},
        {"$set": {"application_status": status, "updated_at": datetime.utcnow()}}
    )

    subject = "Update on Your Job Application"
    body = f"""
    Hello {application['applicant_name']},

    Your job application status has been updated to: {status.upper()}.
    
    Regards,
    Banjo's Restaurant Team
    """
    send_email(application["applicant_email"], subject, body)

    return {"updated": result.modified_count}

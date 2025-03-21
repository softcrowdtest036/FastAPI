# banjos_restaurant\app\models\career.py

from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

def job_application_helper(job_application) -> dict:
    return {
        "id": str(job_application["_id"]),
        "branch_id": job_application["branch_id"],
        "job_title": job_application["job_title"],
        "applicant_name": job_application["applicant_name"],
        "applicant_email": job_application["applicant_email"],
        "applicant_phone": job_application["applicant_phone"],
        "resume_url": job_application["resume_url"],
        "cover_letter": job_application.get("cover_letter"),
        "application_status": job_application["application_status"],
        "created_at": job_application["created_at"],
        "updated_at": job_application["updated_at"],
    }

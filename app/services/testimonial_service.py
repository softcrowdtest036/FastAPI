from app.core.database import mongodb
from app.models.testimonial import Testimonial
from app.utils.email import send_email, render_template
from datetime import datetime
from bson import ObjectId

async def create_testimonial(testimonial_data: dict):
    # Add timestamp and default status
    testimonial_data["created_at"] = datetime.utcnow()
    testimonial_data["status"] = "pending"

    # Insert testimonial into MongoDB
    db = mongodb.get_database()
    result = await db.testimonials.insert_one(testimonial_data)

    # Send confirmation email to the user
    email_body = render_template("testimonial_confirmation.html", name=testimonial_data["name"])
    send_email(testimonial_data["email"], "Thank you for your testimonial!", email_body)

    return str(result.inserted_id)

async def get_testimonial(testimonial_id: str):
    db = mongodb.get_database()
    testimonial = await db.testimonials.find_one({"_id": ObjectId(testimonial_id)})
    if testimonial:
        testimonial["id"] = str(testimonial["_id"])  # Convert ObjectId to str
    return testimonial

async def get_all_testimonials():
    db = mongodb.get_database()
    testimonials = await db.testimonials.find({}).to_list(100)  # Remove the status filter
    
    # Convert ObjectId to string for JSON serialization
    for testimonial in testimonials:
        testimonial["id"] = str(testimonial["_id"])
        del testimonial["_id"]  # Remove the ObjectId field
    
    return testimonials

async def update_testimonial_status(testimonial_id: str, status: str):
    db = mongodb.get_database()
    await db.testimonials.update_one({"_id": ObjectId(testimonial_id)}, {"$set": {"status": status}})
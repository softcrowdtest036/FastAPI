from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime
from app.models.franchise import FranchiseRequestCreate
from fastapi.encoders import jsonable_encoder

async def create_franchise_request(db: AsyncIOMotorDatabase, request_data: FranchiseRequestCreate):
    """Create a new franchise request and send a confirmation email"""
    franchise_dict = jsonable_encoder(request_data)
    franchise_dict["created_at"] = datetime.utcnow()
    franchise_dict["updated_at"] = datetime.utcnow()
    franchise_dict["request_status"] = "pending"

    result = await db.franchise_requests.insert_one(franchise_dict)
    franchise_dict["_id"] = str(result.inserted_id)

    # Send email (ensure send_email function is implemented)
    subject = "✨ Your Franchise Request Has Been Successfully Submitted! ✨"
    body = f"""
    <html>
    <body>
        <h2>Banjo's Restaurant Franchise Application</h2>
        <p>Dear {request_data.user_name},</p>
        <p>We are delighted to confirm the successful submission of your franchise request!</p>
    </body>
    </html>
    """
    # send_email(request_data.user_email, subject, body)  # Uncomment and implement this function

    return franchise_dict

async def get_all_requests(db: AsyncIOMotorDatabase):
    """Retrieve all franchise requests"""
    requests = await db.franchise_requests.find().to_list(None)
    for req in requests:
        req["_id"] = str(req["_id"])  # Convert ObjectId to string
    return requests

async def get_request_by_id(db: AsyncIOMotorDatabase, request_id: str):
    """Retrieve a specific franchise request by ID"""
    try:
        request = await db.franchise_requests.find_one({"_id": ObjectId(request_id)})
        if request:
            request["_id"] = str(request["_id"])  # Fix ObjectId serialization
            return request
        return None
    except Exception:
        return None  # Return None if ID is invalid

async def update_request_status(db: AsyncIOMotorDatabase, request_id: str, status: str):
    """Update franchise request status and notify the user via email"""
    request = await db.franchise_requests.find_one({"_id": ObjectId(request_id)})
    if not request:
        return {"updated": 0}

    result = await db.franchise_requests.update_one(
        {"_id": ObjectId(request_id)},
        {"$set": {"request_status": status, "updated_at": datetime.utcnow()}}
    )

    if result.modified_count > 0:
        # Send email (ensure send_email function is implemented)
        subject = "📢 Important Update: Your Franchise Request Status"
        body = f"""
        <html>
        <body>
            <h2>Franchise Request Status Update</h2>
            <p>Dear {request['user_name']},</p>
            <p>Your franchise request status has been updated to: {status}</p>
        </body>
        </html>
        """
        # send_email(request["user_email"], subject, body)  # Uncomment and implement this function

    return {"updated": result.modified_count}

async def delete_request(db: AsyncIOMotorDatabase, request_id: str):
    """Delete a franchise request"""
    try:
        result = await db.franchise_requests.delete_one({"_id": ObjectId(request_id)})
        return {"deleted": result.deleted_count}
    except Exception:
        return {"deleted": 0} 
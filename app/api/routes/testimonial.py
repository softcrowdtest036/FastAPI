from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form
from app.schemas.testimonial import TestimonialCreate, TestimonialResponse
from app.services.testimonial_service import create_testimonial, get_testimonial, get_all_testimonials, update_testimonial_status
from app.core.config import IMAGES_DIR
import os
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=TestimonialResponse)
async def submit_testimonial(
    name: str = Form(...),
    email: str = Form(...),
    description: str = Form(...),
    rating: int = Form(...),
    image: UploadFile = File(None)
):
    testimonial_data = {
        "name": name,
        "email": email,
        "description": description,
        "rating": rating,
    }

    # Save image if provided
    if image:
        image_path = os.path.join(IMAGES_DIR, f"{datetime.utcnow().timestamp()}_{image.filename}")
        with open(image_path, "wb") as buffer:
            buffer.write(await image.read())
        testimonial_data["image"] = f"/static/images/{os.path.basename(image_path)}"

    # Create testimonial
    testimonial_id = await create_testimonial(testimonial_data)
    return {**testimonial_data, "id": testimonial_id, "status": "pending", "created_at": datetime.utcnow()}

@router.get("/{testimonial_id}", response_model=TestimonialResponse)
async def read_testimonial(testimonial_id: str):
    testimonial = await get_testimonial(testimonial_id)
    if not testimonial:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Testimonial not found")
    return testimonial

@router.get("/", response_model=list[dict])
async def read_all_testimonials():
    testimonials = await get_all_testimonials()
    return testimonials

@router.patch("/{testimonial_id}/status")
async def change_testimonial_status(testimonial_id: str, status: str):
    if status not in ["pending", "approved", "rejected"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid status")
    await update_testimonial_status(testimonial_id, status)
    return {"message": "Testimonial status updated successfully"}
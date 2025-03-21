from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class BranchModel(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    latitude: float
    longitude: float
    address: str
    city: str
    state: Optional[str] = None
    country: str
    zipcode: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    opening_hours: Optional[str] = None
    manager_name: Optional[str] = None
    branch_opening_date: Optional[str] = None
    branch_status: str = "open"
    seating_capacity: Optional[int] = None
    parking_availability: bool = False
    wifi_availability: bool = False
    image_url: Optional[str] = None

    class Config:
        populate_by_name = True 
        from_attributes = True

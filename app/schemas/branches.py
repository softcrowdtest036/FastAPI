from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date

class BranchCreate(BaseModel):
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

class BranchResponse(BaseModel):
    id: str  # Ensure this field is required
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
    branch_status: str
    seating_capacity: Optional[int] = None
    parking_availability: bool
    wifi_availability: bool
    image_url: Optional[str] = None

    class Config:
        from_attributes = True  # Updated from `orm_mode`

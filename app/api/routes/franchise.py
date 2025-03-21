from fastapi import APIRouter, Depends, HTTPException
from app.core.database import mongodb
from app.models.franchise import FranchiseRequestCreate
from app.services.franchise_service import (
    create_franchise_request,
    get_all_requests,
    get_request_by_id,
    update_request_status,
    delete_request,
)

router = APIRouter()

async def get_database():
    """Ensure the database is connected before returning the database instance."""
    if mongodb.database is None:
        await mongodb.connect()
    return mongodb.get_database()

@router.post("/requests/")
async def add_franchise_request(request_data: FranchiseRequestCreate, db=Depends(get_database)):
    """API to create a franchise request"""
    return await create_franchise_request(db, request_data)

@router.get("/requests/")
async def list_franchise_requests(db=Depends(get_database)):
    """API to get all franchise requests"""
    return await get_all_requests(db)

@router.get("/requests/{request_id}")
async def retrieve_franchise_request(request_id: str, db=Depends(get_database)):
    """API to get a franchise request by ID"""
    request = await get_request_by_id(db, request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Franchise request not found")
    return request

@router.put("/requests/{request_id}/status/{status}")
async def modify_request_status(request_id: str, status: str, db=Depends(get_database)):
    """API to update a franchise request status"""
    return await update_request_status(db, request_id, status)

@router.delete("/requests/{request_id}")
async def remove_request(request_id: str, db=Depends(get_database)):
    """API to delete a franchise request"""
    return await delete_request(db, request_id)
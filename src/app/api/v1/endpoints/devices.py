# app/api/v1/endpoints/users.py

from fastapi import APIRouter
from app.services import device_service

router = APIRouter()

@router.get("/")
async def list_users():
    return device_service.get_all_devices()

@router.get("/{device_id}")
async def get_user(device_id: int):
    return device_service.get_device_by_id(device_id)

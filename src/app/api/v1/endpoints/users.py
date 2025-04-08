# app/api/v1/endpoints/users.py

from fastapi import APIRouter
from app.services import user_service

router = APIRouter()

@router.get("/")
async def list_users():
    return user_service.get_all_users()

@router.get("/{user_id}")
async def get_user(user_id: int):
    return user_service.get_user_by_id(user_id)

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_users():
    return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]

@router.get("/{user_id}")
async def get_user(user_id: int):
    return {"id": user_id, "name": "Sample User"}

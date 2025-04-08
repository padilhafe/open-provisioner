from fastapi import APIRouter, Depends, HTTPException
from app.db.dependencies import get_db
from app.schemas.user_schema import UserCreate, UserUpdate, UserOut
from app.services import user_service
from databases import Database

router = APIRouter()

@router.post("/", response_model=UserOut)
async def create(user: UserCreate, db: Database = Depends(get_db)):
    return await user_service.create_user(db, user)

@router.get("/", response_model=list[UserOut])
async def list_all(db: Database = Depends(get_db)):
    return await user_service.get_users(db)

@router.get("/{user_id}", response_model=UserOut)
async def retrieve(user_id: int, db: Database = Depends(get_db)):
    user = await user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserOut)
async def update(user_id: int, user_update: UserUpdate, db: Database = Depends(get_db)):
    user = await user_service.update_user(db, user_id, user_update)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}", status_code=204)
async def delete(user_id: int, db: Database = Depends(get_db)):
    success = await user_service.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")

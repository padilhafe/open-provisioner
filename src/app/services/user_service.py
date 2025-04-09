# app/srecices/user_service.py

from databases import Database
from sqlalchemy import select
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserUpdate
from app.models.user import User

async def create_user(db: Database, user_data: UserCreate) -> User:
    query = User.__table__.insert().values(**user_data.model_dump())
    user_id = await db.execute(query)
    return await get_user_by_id(db, user_id)

async def get_users(db: Database):
    query = select(User)
    rows = await db.fetch_all(query)
    return rows

async def get_user_by_id(db: Database, user_id: int):
    query = select(User).where(User.id == user_id)
    return await db.fetch_one(query)

async def update_user(db: Database, user_id: int, updates: UserUpdate):
    query = (
        User.__table__
        .update()
        .where(User.id == user_id)
        .values(**updates.model_dump(exclude_unset=True))
    )
    await db.execute(query)
    return await get_user_by_id(db, user_id)

async def delete_user(db: Database, user_id: int) -> bool:
    query = User.__table__.delete().where(User.id == user_id)
    result = await db.execute(query)
    return result > 0
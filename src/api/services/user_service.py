# api/srecices/user_service.py

from sqlalchemy import select, update as sqlalchemy_update, delete as sqlalchemy_delete
from sqlalchemy.ext.asyncio import AsyncSession
from api.models.user import User
from api.schemas.user_schema import UserCreate, UserUpdate

async def create_user(session: AsyncSession, user_data: UserCreate) -> User:
    user = User(**user_data.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def get_users(session: AsyncSession):
    result = await session.execute(select(User))
    return result.scalars().all()

async def get_user_by_id(session: AsyncSession, user_id: int):
    result = await session.execute(select(User).where(User.id == user_id))
    return result.scalars().first()

async def update_user(session: AsyncSession, user_id: int, updates: UserUpdate):
    values = updates.model_dump(exclude_unset=True)
    await session.execute(
        sqlalchemy_update(User).where(User.id == user_id).values(**values)
    )
    await session.commit()
    return await get_user_by_id(session, user_id)

async def delete_user(session: AsyncSession, user_id: int) -> bool:
    result = await session.execute(
        sqlalchemy_delete(User).where(User.id == user_id)
    )
    await session.commit()
    return result.rowcount > 0

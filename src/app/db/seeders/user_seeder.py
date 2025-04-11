# app/seeders/user_seeder.py

from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession

async def seed_users(session: AsyncSession):
    existing = await session.execute(User.__table__.select().limit(1))
    if existing.first():
        print("Usuários já existem.")
        return

    users = [
        User(name=f"Admin{i}", email=f"admin{i}@example.com")
        for i in range(5)
    ]
    session.add_all(users)
    await session.commit()
    print("Usuários inseridos com sucesso.")

# app/db/dependencies.py

from app.db.session import async_session

async def get_db():
    async with async_session() as session:
        yield session

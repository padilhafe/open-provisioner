import pytest
import pytest_asyncio
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from app.main import app, lifespan
from app.db.database import database
from app.db.dependencies import get_db
from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv

@pytest_asyncio.fixture
async def client():
    async with lifespan(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac

@pytest_asyncio.fixture(autouse=True)
async def cleanup_database():
    yield
    db = await get_db()
    await db.execute("TRUNCATE TABLE users")

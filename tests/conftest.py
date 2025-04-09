# tests/conftest.py
import pytest
import pytest_asyncio
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from app.main import app, lifespan
from app.db.database import database
from app.db.dependencies import get_db

def pytest_configure(config):
    config.option.asyncio_loop_scope = "session"

@pytest_asyncio.fixture()
async def client():
    async with lifespan(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac

@pytest_asyncio.fixture(autouse=True)
async def cleanup_database():
    yield
    await database.connect()
    async with database.connection() as conn:
        await conn.execute("DELETE FROM devices")
        await conn.execute("DELETE FROM users")
    await database.disconnect()
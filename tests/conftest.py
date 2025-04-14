# tests/conftest.py

import pytest
import pytest_asyncio
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from api.main import app
from api.db.database import database

# Override the default event_loop fixture to have session scope
@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for the entire test session."""
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="session", autouse=True)
async def init_database():
    # Connect to the database
    await database.connect()
    yield
    # Disconnect after all tests are done
    await database.disconnect()

# Fixture for the HTTP client
@pytest_asyncio.fixture(scope="function")
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

# Fixture to clean up the database between tests
@pytest_asyncio.fixture(scope="function", autouse=True)
async def cleanup_database():
    async with database.connection() as conn:
        await conn.execute("DELETE FROM cpes")
        await conn.execute("DELETE FROM customers")
        await conn.execute("DELETE FROM devices")
        await conn.execute("DELETE FROM users")
    yield  # Run the test after cleanup
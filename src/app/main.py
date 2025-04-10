# app/main.py

from fastapi import FastAPI
from app.api.v1.endpoints import users, devices, customers, cpes
from app.db.database import database
from contextlib import asynccontextmanager

# Define the lifespan handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(
    title="OpenProvisioner",
    version="1.0.0",
    lifespan=lifespan
)

# Include routes
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(devices.router, prefix="/api/v1/devices", tags=["Devices"])
app.include_router(customers.router, prefix="/api/v1/customers", tags=["Customers"])
app.include_router(cpes.router, prefix="/api/v1/cpes", tags=["CPEs"])

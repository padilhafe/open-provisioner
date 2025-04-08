from fastapi import FastAPI
from app.api.v1.endpoints import users, devices
from app.db.database import database

app = FastAPI(
    title="OpenProvisioner",
    version="1.0.0",
)

# Include routes
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(devices.router, prefix="/api/v1/devices", tags=["Devices"])

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
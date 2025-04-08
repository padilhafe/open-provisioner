from fastapi import FastAPI
from app.api.v1.endpoints import users, devices

app = FastAPI(
    title="OpenProvisioner",
    version="1.0.0",
)

# Include routes
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(devices.router, prefix="/api/v1/devices", tags=["Devices"])

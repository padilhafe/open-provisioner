# app/schemas/cpe_schema.py

from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.schemas.device_schema import DeviceOut

class CpeCreate(BaseModel):
    cpe_type: str
    state: Optional[str] = None
    customer_id: int
    device_id: int

class CpeUpdate(BaseModel):
    cpe_type: Optional[str] = None
    state: Optional[str] = None
    customer_id: Optional[int] = None
    device_id: Optional[int] = None

class CpeOut(BaseModel):
    id: int
    cpe_type: str
    state: Optional[str] = None
    customer_id: int
    device_id: int
    device: Optional[DeviceOut] = None

    model_config = ConfigDict(from_attributes=True)

# app/schemas/customer_schema.py

from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.schemas.cpe_schema import CpeOut

class CustomerCreate(BaseModel):
    name: str
    username: Optional[str] = None
    integration_id: Optional[int] = None

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    integration_id: Optional[int] = None

class CustomerOut(BaseModel):
    id: int
    name: str
    username: Optional[str] = None
    integration_id: Optional[int] = None
    cpe: Optional[CpeOut] = None

    model_config = ConfigDict(from_attributes=True)

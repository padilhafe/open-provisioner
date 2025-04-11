# app/schemas/customer_schema.py

from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.schemas.cpe_schema import CpeOut
from app.core.types import CUSTOMER_STATUS

class CustomerCreate(BaseModel):
    name: str
    username: str
    status: str = CUSTOMER_STATUS[0]
    integration_id: Optional[int] = None

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    username: str
    status: str = CUSTOMER_STATUS[0]
    integration_id: Optional[int] = None

class CustomerOut(BaseModel):
    id: int
    name: str
    username: str
    status: str = CUSTOMER_STATUS[0]
    integration_id: Optional[int] = None
    cpe: Optional[CpeOut] = None

    model_config = ConfigDict(from_attributes=True)

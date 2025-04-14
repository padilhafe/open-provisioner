# api/schemas/cpe_schema.py

from pydantic import BaseModel, Field, ConfigDict, validator
from typing import Optional
from api.schemas.device_schema import DeviceOut
from api.core.enums import GponOperState

class CpeCreate(BaseModel):
    cpe_type: str
    oper_state: GponOperState = Field(default=GponOperState.InitialState)
    customer_id: int
    device_id: int

    @validator('oper_state', pre=True)
    def convert_oper_state(cls, v):
        if isinstance(v, str):
            return GponOperState[v].value
        return v.value if isinstance(v, GponOperState) else v

class CpeUpdate(BaseModel):
    cpe_type: Optional[str] = None
    oper_state: Optional[GponOperState] = None
    customer_id: Optional[int] = None
    device_id: Optional[int] = None

    @validator('oper_state', pre=True)
    def convert_oper_state(cls, v):
        if v is None:
            return None
        if isinstance(v, str):
            return GponOperState[v].value
        return v.value if isinstance(v, GponOperState) else v

class CpeOut(BaseModel):
    id: int
    cpe_type: str
    oper_state: GponOperState
    customer_id: int
    device_id: int
    device: Optional[DeviceOut] = None

    model_config = ConfigDict(from_attributes=True)
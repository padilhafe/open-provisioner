# app/schemas/device_schema.py

from pydantic import BaseModel, ConfigDict
from ipaddress import IPv4Address
from typing import Optional
from app.core.enums import SnmpVersion

class DeviceCreate(BaseModel):
    name: str
    device_type: str
    mgmt_ipv4: IPv4Address
    snmp_version: SnmpVersion
    snmp_community: str

class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    device_type: Optional[str] = None
    mgmt_ipv4: Optional[IPv4Address] = None
    snmp_version: Optional[SnmpVersion] = None
    snmp_community: Optional[str] = None

class DeviceOut(BaseModel):
    id: int
    name: str
    device_type: str
    mgmt_ipv4: IPv4Address
    snmp_version: SnmpVersion
    snmp_community: str

    model_config = ConfigDict(from_attributes=True)

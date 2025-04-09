# app/schemas/device_schema.py

from pydantic import BaseModel, EmailStr, ConfigDict
from ipaddress import IPv4Address
from app.core.enums import DeviceType, SnmpVersion

class DeviceCreate(BaseModel):
    name: str
    device_type: DeviceType
    mgmt_ipv4: IPv4Address
    snmp_version: SnmpVersion
    snmp_community: str

class DeviceUpdate(BaseModel):
    name: str | None = None
    device_type: DeviceType | None = None
    mgmt_ipv4: IPv4Address | None = None
    snmp_version: SnmpVersion | None = None
    snmp_community: str

class DeviceOut(BaseModel):
    id: int
    name: str
    device_type: DeviceType
    mgmt_ipv4: IPv4Address
    snmp_version: SnmpVersion
    snmp_community: str

    model_config = ConfigDict(
        from_attributes=True
    )

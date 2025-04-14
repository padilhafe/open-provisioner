# api/schemas/device_schema.py

from pydantic import BaseModel, ConfigDict
from ipaddress import IPv4Address
from typing import Optional
from api.core.enums import SnmpVersion

class DeviceCreate(BaseModel):
    hostname: str
    device_type: str
    device_hostname: Optional[str] = None

    device_mgmt_ipv4: Optional[IPv4Address] = None
    device_username: Optional[str] = None
    device_password: Optional[str] = None
    device_mgmt_port: int = 22
    
    snmp_version: SnmpVersion
    snmp_port: int
    snmp_community: str

class DeviceUpdate(BaseModel):
    hostname: Optional[str] = None
    device_type: Optional[str] = None
    device_hostname: Optional[str] = None

    device_mgmt_ipv4: Optional[IPv4Address] = None
    device_username: Optional[str] = None
    device_password: Optional[str] = None
    device_mgmt_port: int = 22
    
    snmp_version: Optional[SnmpVersion] = None
    snmp_community: Optional[str] = None

class DeviceOut(BaseModel):
    id: int
    hostname: str
    device_type: str
    device_hostname: Optional[str] = None
    
    device_mgmt_ipv4: IPv4Address
    device_username: str
    device_password: str
    device_mgmt_port: int
    
    snmp_version: SnmpVersion
    snmp_port: int
    snmp_community: str

    model_config = ConfigDict(from_attributes=True)

# src/app/core/enums.py

from enum import Enum

class DeviceType(str, Enum):
    ROUTER = "router"
    SWITCH = "switch"
    OLT = "olt"

class SnmpVersion(int, Enum):
    V1 = 1
    V2 = 2
    V3 = 3

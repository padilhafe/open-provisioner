# src/app/core/enums.py

from enum import Enum

# Users Enums
class UserRoles(str, Enum):
    OPERATOR = "operator"
    TECHINICIAN = "techinician"
    ADMIN = "admin"

# Device and CPE Enums
class DeviceType(str, Enum):
    ROUTER = "router"
    SWITCH = "switch"
    OLT = "olt"

class CpeType(str, Enum):
    WIFI_ROUTER = "wifi_router"
    ONU = "onu"
    ONT = "ont"

# Configuration Enums
class SnmpVersion(int, Enum):
    V1 = 1
    V2 = 2
    V3 = 3

class GponOperState(str, Enum):
    InitialState = 1
    StandByState = 2
    SerialNumberState = 3
    RangingState = 4
    OperationState = 5
    PopupState = 6
    EmergencyStopState = 7
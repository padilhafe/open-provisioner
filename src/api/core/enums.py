# api/core/enums.py

from enum import Enum

class SnmpVersion(int, Enum):
    V1 = 1
    V2 = 2
    V3 = 3

class GponOperState(int, Enum):
    InitialState = 1
    StandByState = 2
    SerialNumberState = 3
    RangingState = 4
    OperationState = 5
    PopupState = 6
    EmergencyStopState = 7

class OpenBmcPowerActions(str, Enum):
    on = "On"
    force_off = "ForceOff"
    force_restart = "ForceRestart"

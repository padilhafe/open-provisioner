# app/models/device.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from typing import Optional
from app.models import Base

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    hostname = Column(String(100), nullable=False)
    device_type = Column(String(32), nullable=False)
    
    device_mgmt_ipv4: Optional[str] = Column(String(16), unique=True, nullable=True)
    device_username: Optional[str] = Column(String(32), nullable=True)
    device_password: Optional[str] = Column(String(32), nullable=True)
    device_mgmt_port: int = Column(Integer, nullable=False, default=22)

    snmp_version: Optional[int] = Column(Integer, nullable=True)
    snmp_port: int = Column(Integer, nullable=False, default=161)
    snmp_community: Optional[str] = Column(String(32), nullable=True)

    cpes = relationship("Cpe", back_populates="device", lazy="selectin")

# app/models/device.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from typing import Optional
from app.models import Base

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    device_type = Column(String(32), index=True, nullable=False)
    mgmt_ipv4: Optional[str] = Column(String(16), unique=True, index=True, nullable=True)
    snmp_version: Optional[int] = Column(Integer, index=True, nullable=True)
    snmp_community: Optional[str] = Column(String(32), index=True, nullable=True)

    cpes = relationship("Cpe", back_populates="device", lazy="selectin")

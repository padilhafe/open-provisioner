# app/models/cpe.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models import Base

class Cpe(Base):
    __tablename__ = "cpes"

    id = Column(Integer, primary_key=True)
    cpe_type = Column(String)
    state = Column(String)
    customer_id = Column(Integer, ForeignKey("customers.id"), unique=True)
    device_id = Column(Integer, ForeignKey("devices.id"))

    customer = relationship("Customer", back_populates="cpe")
    device = relationship("Device", back_populates="cpes")

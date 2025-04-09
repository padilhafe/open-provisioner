# app/models/cpe.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models import Base

class Cpe(Base):
    __tablename__ = "cpes"

    id = Column(Integer, primary_key=True, index=True)

    # Foreign keys
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)

    # Relationships
    customer = relationship("Customer", back_populates="cpe")
    device = relationship("Device", back_populates="cpes")
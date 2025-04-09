# app/models/customer.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    username = Column(String(100), nullable=True)
    integration_id = Column(Integer, nullable=True)

    # Customer has one CPE
    cpe = relationship("CPE", back_populates="customer", uselist=False)
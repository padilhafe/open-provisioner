# app/models/customer.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models import Base
from app.core.types import CUSTOMER_STATUS

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    username = Column(String(100), nullable=True, unique=True)
    status = Column(String(32), nullable=False, default=CUSTOMER_STATUS[0])
    integration_id = Column(Integer, nullable=True)

    cpe = relationship("Cpe", back_populates="customer", uselist=False, lazy="selectin")

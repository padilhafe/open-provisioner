# api/models/cpe.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum
from api.models import Base
from api.core.enums import GponOperState
from api.core.types import CPE_TYPE

class Cpe(Base):
    __tablename__ = "cpes"

    id = Column(Integer, primary_key=True)
    cpe_type = Column(String(32), nullable=False, default=CPE_TYPE[0])
    oper_state = Column(Integer, nullable=False, default=GponOperState.InitialState.value)
    customer_id = Column(Integer, ForeignKey("customers.id"), unique=True)
    device_id = Column(Integer, ForeignKey("devices.id"))

    customer = relationship("Customer", back_populates="cpe", lazy="selectin")
    device = relationship("Device", back_populates="cpes", lazy="selectin")

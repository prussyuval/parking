from sqlalchemy import Column, JSON, Integer
from sqlalchemy.dialects.postgresql import UUID

from models.base import Model


class ParkingLot(Model):
    __tablename__ = "parking_lots"

    id: int = Column(UUID(as_uuid=True), unique=True, nullable=False)

    hour: int = Column(Integer(), nullable=False)
    minute: int = Column(Integer(), nullable=False)
    day: int = Column(Integer(), nullable=False)

    status: dict = Column(JSON(), nullable=False, default={})


ParkingLotTable = ParkingLot.__table__

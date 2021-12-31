from typing import List

from sqlalchemy import Column, JSON, Integer, String, ARRAY

from models.base import Model


class Lot(Model):
    __tablename__ = "lots"

    id: int = Column(Integer(), unique=True, nullable=False, primary_key=True)
    lot_id: int = Column(Integer(), unique=True, nullable=False)
    eng_name: str = Column(String(), nullable=False)
    heb_name: str = Column(String(), nullable=False)
    address: str = Column(String(), nullable=False)
    nicknames: List[str] = Column(ARRAY(String()), nullable=True)


class ParkingLot(Model):
    __tablename__ = "parking_lots"

    id: int = Column(Integer(), unique=True, nullable=False, primary_key=True)

    lot_id: int = Column(Integer(), unique=True, nullable=False)

    hour: int = Column(Integer(), nullable=False)
    minute: int = Column(Integer(), nullable=False)
    day: int = Column(Integer(), nullable=False)

    status: dict = Column(JSON(), nullable=False, default={})

    # update_date: datetime = Column(DateTime(), nullable=True, default=datetime.now())


class ParkingLotView(Model):
    __tablename__ = "parking_lot_views"

    id: int = Column(Integer(), unique=True, nullable=False, primary_key=True)
    lot_id: int = Column(Integer(), unique=True, nullable=False)
    heat_map_data: dict = Column(JSON(), nullable=False, default={})


LotTable = Lot.__table__
ParkingLotTable = ParkingLot.__table__
ParkingLotViewTable = ParkingLotView.__tablename__

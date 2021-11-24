from sqlalchemy import Column, Integer, String

from models.base import Model


class Traffic(Model):
    __tablename__ = "traffic"

    ip: int = Column(String(), unique=True, nullable=False, primary_key=True)
    entrances: int = Column(Integer(), unique=True, default=0)


TrafficTable = Traffic.__table__

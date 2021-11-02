from typing import Optional

from aiopg.sa.result import RowProxy
from sqlalchemy import and_

from models.parking_lot import ParkingLotTable
from utils.logging import logger
from utils.postgres.db import DatabaseConnection


class ParkingLotApi:
    @staticmethod
    async def get_status(lot_id: int, day: int, hour: int, minute: int) -> Optional[RowProxy]:
        async with DatabaseConnection.acquire_connection() as connection:
            result = await connection.execute(ParkingLotTable.select().where(
                and_(ParkingLotTable.c.id == lot_id,
                     ParkingLotTable.c.minute == minute,
                     ParkingLotTable.c.hour == hour,
                     ParkingLotTable.c.day == day)
            ))

            return await result.fetchone()

    @staticmethod
    async def update_status(lot_id: int, day: int, hour: int, minute: int, status: dict) -> None:
        logger.debug(f"Updating status for lot {lot_id} ({day} {hour}:{minute}).")
        async with DatabaseConnection.acquire_connection() as connection:
            await connection.execute(ParkingLotTable
                                     .update()
                                     .where(and_(ParkingLotTable.c.id == lot_id,
                                                 ParkingLotTable.c.minute == minute,
                                                 ParkingLotTable.c.hour == hour,
                                                 ParkingLotTable.c.day == day))
                                     .values(dict(status=status)))

    @staticmethod
    async def create_status(lot_id: int, day: int, hour: int, minute: int, status: dict) -> RowProxy:
        status_data = dict(id=lot_id, day=day, hour=hour, minute=minute, status=status)

        logger.info(f"Inserting lot statistics of lot {lot_id} into db ({day} {hour}:{minute})")
        async with DatabaseConnection.acquire_connection() as connection:
            new_review = await connection.execute(ParkingLotTable.insert()
                                                  .values(**status_data)
                                                  .returning(ParkingLotTable.c.id))

            return await new_review.first()

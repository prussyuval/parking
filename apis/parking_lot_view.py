from models.parking_lot import ParkingLotViewTable
from utils.logging import logger
from utils.postgres.db import DatabaseConnection


class ParkingLotViewApi:
    @staticmethod
    async def create_view(lot_id: int, heat_map_data: dict):
        view_data = dict(lot_id=lot_id, heat_map_data=heat_map_data)

        logger.info(f"Inserting lot view statistics of lot {lot_id} into db")
        async with DatabaseConnection.acquire_connection() as connection:
            await connection.execute(ParkingLotViewTable.insert().values(**view_data))

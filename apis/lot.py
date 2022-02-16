from typing import Optional, List

from aiopg.sa.result import RowProxy
from sqlalchemy import or_

from models.parking_lot import ParkingLotTable, LotTable
from utils.postgres.db import DatabaseConnection


class LotApi:
    @staticmethod
    async def search_lot(phrase: str) -> Optional[RowProxy]:
        search_statement = f"%{phrase}%"
        async with DatabaseConnection.acquire_connection() as connection:
            results = await connection.execute(LotTable.select().where(
                or_(LotTable.c.address.ilike(search_statement),
                    LotTable.c.heb_name.ilike(search_statement),
                    LotTable.c.eng_name.ilike(search_statement)
                    # TODO yuval add nicknames
                    )
            ))

            return await results.fetchall()

    @staticmethod
    async def get_lot_ids() -> List[int]:
        async with DatabaseConnection.acquire_connection() as connection:
            results = await connection.execute(LotTable.select())
            results = await results.fetchall()
        return [r["lot_id"] for r in results]

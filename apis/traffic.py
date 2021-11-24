from models.traffic import TrafficTable
from utils.postgres.db import DatabaseConnection


class TrafficApi:
    @staticmethod
    async def increase_ip_entrances(ip: str) -> None:
        if not ip:
            return

        async with DatabaseConnection.acquire_connection() as connection:
            result = await connection.execute(TrafficTable.select().where(TrafficTable.c.ip == ip))
            current_value = await result.fetchone()

        if current_value is None:
            traffic_data = dict(entrances=1, ip=ip)
            await connection.execute(TrafficTable.insert().values(**traffic_data))
        else:
            entrances = dict(result)["entrances"] + 1
            await connection.execute(TrafficTable.update().where(TrafficTable.c.ip == ip).values(dict(entrances=entrances)))

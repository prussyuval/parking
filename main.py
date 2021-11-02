import asyncio
from datetime import datetime

from apis.external.ahuzot_api import AhuzotApi
from apis.parking_lot import ParkingLotApi
from enums import Status
from utils.logging import logger

LOT_IDS = [45]


async def query_parking_lots():
    for lot_id in LOT_IDS:
        try:
            current_status, query_time = await AhuzotApi.query_status(lot_id)
        except:
            logger.warning(f"Failed to receive status on {datetime.now()}")
            continue

        existing_result = await ParkingLotApi.get_status(lot_id=lot_id,
                                                         day=query_time.weekday(),
                                                         hour=query_time.hour,
                                                         minute=query_time.minute)

        if existing_result is None:
            status = {Status.empty.value: 0, Status.few_left.value: 0, Status.full.value: 0}
            status[current_status.value] += 1

            await ParkingLotApi.create_status(lot_id=lot_id,
                                              day=query_time.weekday(),
                                              hour=query_time.hour,
                                              minute=query_time.minute,
                                              status=status)

        else:
            dict_result = dict(existing_result)
            status = dict_result["status"]
            status[current_status.value] += 1
            await ParkingLotApi.update_status(lot_id=lot_id,
                                              day=query_time.weekday(),
                                              hour=query_time.hour,
                                              minute=query_time.minute,
                                              status=status)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(query_parking_lots())

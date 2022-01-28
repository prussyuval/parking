import asyncio
from datetime import datetime

from apis.external.ahuzot_api import AhuzotApi
from apis.lot import LotApi
from apis.parking_lot import ParkingLotApi
from utils.logging import logger
from utils.time_serialize import datetime_to_str


async def query_parking_lots():
    lot_ids = await LotApi.get_lot_ids()
    for lot_id in lot_ids:
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
            status = {
                datetime_to_str(query_time): current_status.value,
            }
            await ParkingLotApi.create_status(lot_id=lot_id,
                                              day=query_time.weekday(),
                                              hour=query_time.hour,
                                              minute=query_time.minute,
                                              status=status)

        else:
            dict_result = dict(existing_result)
            status = dict_result["status"]
            if datetime_to_str(query_time) in status:
                logger.warning(f"Time {query_time} already exists in the db")
                return

            status[datetime_to_str(query_time)] = current_status.value
            await ParkingLotApi.update_status(lot_id=lot_id,
                                              day=query_time.weekday(),
                                              hour=query_time.hour,
                                              minute=query_time.minute,
                                              status=status)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    while True:
        start_time = datetime.now()
        loop.run_until_complete(query_parking_lots())
        end_time = datetime.now()
        delta_time = end_time - start_time
        logger.info(f"Sleeping for {60 - delta_time.total_seconds()} seconds")
        loop.run_until_complete(asyncio.sleep(60 - delta_time.total_seconds()))

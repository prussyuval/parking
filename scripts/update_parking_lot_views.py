import asyncio
from collections import defaultdict

from apis.parking_lot_view import ParkingLotViewApi
from enums import Status, STATUS_TO_SCORE
from lot_ids import LOT_IDS

from apis.parking_lot import ParkingLotApi
from utils.time_serialize import time_with_dow_to_str


async def update_parking_lot_views():
    for lot_id in LOT_IDS:
        results = await ParkingLotApi.get_parking_lot_full_data(lot_id=lot_id)

        heat_map_data = defaultdict(float)

        for result in results:
            dict_result = dict(result)
            statuses = dict_result["status"]
            score = 0
            total = 0
            for status in statuses.values():
                status = Status(status)
                status_score = STATUS_TO_SCORE.get(status)
                if status_score is not None:
                    score += status_score
                    total += 1

            heat_map_data[time_with_dow_to_str(dict_result["day"], dict_result["hour"], dict_result["minute"])] = (
                round(score / total, 2)
            )

        await ParkingLotViewApi.create_view(lot_id, dict(heat_map_data))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(update_parking_lot_views())

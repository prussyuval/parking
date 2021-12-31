import asyncio
from dataclasses import dataclass

from apis.parking_lot_view import ParkingLotViewApi
from enums import Status, STATUS_TO_SCORE
from lot_ids import LOT_IDS

from apis.parking_lot import ParkingLotApi


@dataclass
class HourScore:
    score_sum: float = 0.0
    score_count: float = 0.0

    def get_score_avg(self) -> float:
        return round(self.score_sum / self.score_count, 2)


async def update_parking_lot_views():
    for lot_id in LOT_IDS:
        results = await ParkingLotApi.get_parking_lot_full_data(lot_id=lot_id)

        heat_map_data = dict()

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

            day = dict_result["day"]
            hour = dict_result["hour"]

            if day not in heat_map_data:
                heat_map_data[day] = {}

            if hour not in heat_map_data[day]:
                heat_map_data[day][hour] = HourScore()

            heat_map_data[day][hour].score_sum += score
            heat_map_data[day][hour].score_sum += total

        for day, day_data in heat_map_data.items():
            for hour, hour_data in day_data.items():
                day_data[hour] = hour_data.get_score_avg()
        await ParkingLotViewApi.create_view(lot_id, dict(heat_map_data))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(update_parking_lot_views())

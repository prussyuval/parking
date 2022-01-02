import asyncio
from dataclasses import dataclass

from apis.parking_lot_view import ParkingLotViewApi
from enums import Status
from lot_ids import LOT_IDS

from apis.parking_lot import ParkingLotApi


@dataclass
class HourScore:
    full: int = 0
    few_left: int = 0
    empty: int = 0

    def get_score(self) -> float:
        total = self.full + self.few_left + self.empty

        if self.full == total:
            return 100

        if self.few_left == total:
            return 99

        if self.empty == total:
            return 0

        full_cardinality = self.full / total
        few_left_cardinality = self.few_left / total
        empty_cardinality = self.empty / total

        return 100 * (full_cardinality + (few_left_cardinality) * 0.95 + (empty_cardinality) * 0.05)


async def update_parking_lot_views():
    for lot_id in LOT_IDS:
        results = await ParkingLotApi.get_parking_lot_full_data(lot_id=lot_id)

        heat_map_data = dict()

        for result in results:
            dict_result = dict(result)
            statuses = dict_result["status"]

            day = dict_result["day"]
            hour = float(dict_result["hour"])
            minute = dict_result["minute"]
            if minute >= 30:
                hour += 0.5

            if day not in heat_map_data:
                heat_map_data[day] = {}

            if hour not in heat_map_data[day]:
                heat_map_data[day][hour] = HourScore()

            for status in statuses.values():
                status = Status(status)
                if status == Status.full:
                    heat_map_data[day][hour].full += 1
                elif status == Status.empty:
                    heat_map_data[day][hour].empty += 1
                elif status == Status.few_left:
                    heat_map_data[day][hour].few_left += 1

        for day, day_data in heat_map_data.items():
            for hour, hour_data in day_data.items():
                day_data[hour] = round(hour_data.get_score(), 2)
        await ParkingLotViewApi.create_view(lot_id, dict(heat_map_data))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(update_parking_lot_views())

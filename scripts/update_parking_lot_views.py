import asyncio
from collections import OrderedDict
from datetime import datetime, timedelta
from typing import Optional, List, Tuple, Dict

from apis.lot import LotApi
from apis.parking_lot_view import ParkingLotViewApi
from enums import Status

from apis.parking_lot import ParkingLotApi
from utils.time_serialize import str_to_datetime


def _calculate_avg_score(scores: List[float]) -> float:
    return round(sum(scores) / len(scores), 2)


async def _collect_data(lot_id: int) -> OrderedDict:
    results = await ParkingLotApi.get_parking_lot_full_data(lot_id=lot_id)

    parking_status = dict()

    for result in results:
        dict_result = dict(result)
        statuses = dict_result["status"]

        for query_time, status in statuses.items():
            parking_status[str_to_datetime(query_time)] = Status(status)

    return OrderedDict(
        sorted(parking_status.items(), key=lambda x: x[0])
    )


def _find_gaps(parking_status: OrderedDict) -> List[datetime]:
    gaps = []
    previous_full = None
    first = True

    for query_time, s in parking_status.items():
        if first:
            first = False
            previous_full = s.is_full_state()
            continue

        if (not previous_full and s.is_full_state()) or (previous_full and not s.is_full_state()):
            gaps.append(query_time)

        previous_full = s.is_full_state()

    return gaps


def _get_next_gap_time(query_time: datetime, gaps: List[datetime]) -> Tuple[Optional[datetime], Optional[timedelta]]:
    """
    >>> _get_next_gap_time(datetime(2021, 11, 10, 14, 1), [datetime(2021, 11, 10, 14, 2), datetime(2021, 11, 10, 14, 9), datetime(2021, 11, 10, 14, 14), datetime(2021, 11, 11, 10, 13), datetime(2021, 11, 11, 14, 21), datetime(2021, 11, 11, 19, 2), datetime(2021, 11, 11, 20, 30)])
    (None, None)
    >>> _get_next_gap_time(datetime(2021, 11, 11, 15, 21), [datetime(2021, 11, 10, 14, 2), datetime(2021, 11, 10, 14, 9), datetime(2021, 11, 10, 14, 14), datetime(2021, 11, 11, 10, 13), datetime(2021, 11, 11, 14, 21), datetime(2021, 11, 11, 19, 2), datetime(2021, 11, 11, 20, 30)])
    (datetime.datetime(2021, 11, 11, 19, 2), datetime.timedelta(seconds=16860))
    >>> _get_next_gap_time(datetime(2021, 11, 11, 20, 31), [datetime(2021, 11, 10, 14, 2), datetime(2021, 11, 10, 14, 9), datetime(2021, 11, 10, 14, 14), datetime(2021, 11, 11, 10, 13), datetime(2021, 11, 11, 14, 21), datetime(2021, 11, 11, 19, 2), datetime(2021, 11, 11, 20, 30)])
    (None, None)
    """
    end = None
    end_i = None
    for i, gap in enumerate(gaps):
        if query_time <= gap:
            end = gap
            end_i = i
            break

    if end is None or end_i in [0, None]:
        return None, None

    start_i = end_i - 1
    start = gaps[start_i]

    return end, end - start


def _get_default_occupation_by_gap_time(gap_timedelta: timedelta) -> float:
    if gap_timedelta < timedelta(minutes=5):
        return 98.0

    if gap_timedelta < timedelta(minutes=15):
        return 95.0

    if gap_timedelta < timedelta(minutes=30):
        return 90.0

    if gap_timedelta < timedelta(hours=1):
        return 80.0

    if gap_timedelta < timedelta(hours=2):
        return 70.0

    if gap_timedelta < timedelta(hours=4):
        return 60.0

    if gap_timedelta < timedelta(hours=6):
        return 50.0

    return 40.0


def _calculate_score(query_time, gaps, parking_status) -> Optional[float]:
    next_gap_time, gap_length = _get_next_gap_time(query_time, gaps)
    if next_gap_time is None or gap_length is None:
        return None

    gap_status: Status = parking_status[next_gap_time]

    if not gap_status.is_full_state():
        # It's a full gap
        return 100.0

    minimum_occupation_at_gap = _get_default_occupation_by_gap_time(gap_length)

    middle_time = next_gap_time - (gap_length / 2)

    if query_time >= middle_time:
        distance_from_gap_center = query_time - middle_time
    else:
        distance_from_gap_center = middle_time - query_time

    relation = abs(float(distance_from_gap_center.total_seconds()) / (float(gap_length.total_seconds()) / 2))
    if relation > 1:
        print()
        print(f"query_time => {query_time}")
        print(f"next_gap_time => {next_gap_time}")
        print(f"gap_length => {gap_length}")
        print(f"relation => {relation}")
        print(f"minimum_occupation_at_gap => {minimum_occupation_at_gap}")
        print(f"distance_from_gap_center => {distance_from_gap_center}")
        print()

    return minimum_occupation_at_gap + (relation * (100 - minimum_occupation_at_gap))


def _calculate_scores(parking_status: OrderedDict, gaps: List[datetime]) -> Dict[int, Dict[float, List[float]]]:
    heat_map_data = dict()

    for query_time, status in parking_status.items():
        score = _calculate_score(query_time, gaps, parking_status)
        if score is None:
            continue

        day = query_time.weekday()
        hour = query_time.hour
        minute = query_time.minute

        if minute >= 30:
            hour += 0.5

        if day not in heat_map_data:
            heat_map_data[day] = {}

        if hour not in heat_map_data[day]:
            heat_map_data[day][hour] = []

        heat_map_data[day][hour].append(score)

    return heat_map_data


async def _create_view(lot_id: int, heat_map_data: Dict[int, Dict[float, List[float]]]):
    for day, day_data in heat_map_data.items():
        for hour, scores in day_data.items():
            day_data[hour] = _calculate_avg_score(scores)
    print(heat_map_data)

    await ParkingLotViewApi.create_view(lot_id, dict(heat_map_data))


async def update_parking_lot_views():
    lot_ids = await LotApi.get_lot_ids()
    for lot_id in lot_ids:
        parking_status = await _collect_data(lot_id)
        gaps = _find_gaps(parking_status)
        heat_map_data = _calculate_scores(parking_status, gaps)
        await _create_view(lot_id, heat_map_data)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(update_parking_lot_views())

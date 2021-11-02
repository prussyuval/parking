import asyncio
from datetime import datetime

from enums import Status
from apis.parking_lot import ParkingLotApi

FILE = "/home/ubuntu/parking2/results.txt"

if __name__ == "__main__":
    with open(FILE, "r") as f:
        lines = f.readlines()

    loop = asyncio.get_event_loop()

    for line in lines:
        current_status = Status(int(line.strip().split("|")[0]))
        query_time = datetime.strptime(line.strip().split("|")[1], "%m/%d/%Y, %H:%M:%S")

        if current_status != Status.unknown:
            status = {str(Status.empty.value): 0, str(Status.few_left.value): 0, str(Status.full.value): 0}
            status[str(current_status.value)] += 1
            task = ParkingLotApi.create_status(lot_id=45,
                                               day=query_time.weekday(),
                                               hour=query_time.hour,
                                               minute=query_time.minute,
                                               status=status)
            loop.run_until_complete(task)

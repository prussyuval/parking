import time
from datetime import datetime
from typing import Tuple

import aiohttp
from bs4 import BeautifulSoup

from enums import Status

URL = "http://www.ahuzot.co.il/Parking/ParkingDetails/?ID={}"

IMAGE_TO_STATUS_MAPPING = {
    "/pics/ParkingIcons/panui.png": Status.empty,
    "/pics/ParkingIcons/meat.png": Status.few_left,
    "/pics/ParkingIcons/male.png": Status.full,
}


class AhuzotApi:
    @classmethod
    async def query_status(cls, lot_id: int) -> Tuple[Status, datetime]:
        async with aiohttp.ClientSession() as session:
            async with session.get(URL.format(lot_id)) as response:
                content = await response.text()

        site_soup = BeautifulSoup(content)

        status_table = site_soup.select_one(".ParkingDetailsTable")
        site_time = status_table.select_one(".IconText").text
        query_time = datetime.strptime(site_time, '%d/%m/%Y %H:%M')
        image_url = status_table.select_one("img").attrs.get("src")
        return IMAGE_TO_STATUS_MAPPING.get(image_url, Status.unknown), query_time

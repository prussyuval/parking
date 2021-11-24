import re
from datetime import datetime, timedelta

import pytz
from aiohttp.web_response import Response

from apis.external.ahuzot_api import AhuzotApi
from apis.parking_lot import ParkingLotApi
from apis.traffic import TrafficApi
from enums import STATUS_NAMING_MAP
from rest_server.resources import CorsFixedResource
from rest_server.response_codes import HttpResponseCode
from rest_server.rest_utils import create_error_response, create_success_response, RestError
from utils.time_serialize import datetime_to_str


class StatusResource(CorsFixedResource):
    async def get(self) -> Response:
        await TrafficApi.increase_ip_entrances(self.request.remote)

        lot_id = self.request.query.get('lot_id')
        if lot_id is None:
            return create_error_response(RestError.MISSING_ARGUMENT,
                                         error_code=HttpResponseCode.BAD_REQUEST,
                                         argument='lot id')
        current_datetime = datetime.now(tz=pytz.timezone("Asia/Jerusalem"))

        current_status, _ = await AhuzotApi.query_status(int(lot_id))

        response_data = {"current": STATUS_NAMING_MAP[current_status], "stored_status": {}, "time": datetime_to_str(current_datetime)}

        result = await ParkingLotApi.get_status(int(lot_id),
                                                current_datetime.weekday(),
                                                current_datetime.hour,
                                                current_datetime.minute)

        if result is not None:
            dict_result = dict(result)
            response_data["stored_status"] = dict_result["status"]

        future_datetime = current_datetime + timedelta(minutes=30)

        result = await ParkingLotApi.get_prediction(int(lot_id),
                                                    future_datetime.weekday(),
                                                    future_datetime.hour,
                                                    future_datetime.minute)

        if result is not None:
            dict_result = dict(result)
            response_data["future_status"] = dict_result["status"]

        return create_success_response(response_data)


class PredictStatusResource(CorsFixedResource):
    @staticmethod
    def _from_str_to_timedelta(delta: str) -> timedelta:
        t = datetime.strptime(delta, "%H:%M")
        return timedelta(hours=t.hour, minutes=t.minute)

    async def get(self) -> Response:
        lot_id = self.request.query.get('lot_id')
        if lot_id is None:
            return create_error_response(RestError.MISSING_ARGUMENT,
                                         error_code=HttpResponseCode.BAD_REQUEST,
                                         argument='lot id')

        delta = self.request.query.get('delta')

        if delta is None:
            return create_error_response(RestError.MISSING_ARGUMENT,
                                         error_code=HttpResponseCode.BAD_REQUEST,
                                         argument='delta')

        try:
            time_delta = self._from_str_to_timedelta(delta)
        except:
            return create_error_response(RestError.INVALID_FORMAT,
                                         error_code=HttpResponseCode.BAD_REQUEST,
                                         argument='delta')


        current_datetime = datetime.now(tz=pytz.timezone("Asia/Jerusalem"))
        prediction_datetime = current_datetime + time_delta

        response_data = {"prediction_time": {}}

        result = await ParkingLotApi.get_status(int(lot_id),
                                                prediction_datetime.weekday(),
                                                prediction_datetime.hour,
                                                prediction_datetime.minute)

        if result is not None:
            dict_result = dict(result)
            response_data["prediction_time"] = dict_result["status"]

        return create_success_response(response_data)

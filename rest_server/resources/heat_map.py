from aiohttp.web_response import Response

from apis.parking_lot_view import ParkingLotViewApi
from rest_server.resources import CorsFixedResource
from rest_server.response_codes import HttpResponseCode
from rest_server.rest_utils import create_error_response, RestError, create_success_response


class LotHeatMapResource(CorsFixedResource):
    async def get(self) -> Response:
        lot_id = self.request.query.get('lot_id')
        if lot_id is None:
            return create_error_response(RestError.MISSING_ARGUMENT,
                                         error_code=HttpResponseCode.BAD_REQUEST,
                                         argument='lot id')

        response_data = {"heat_map": {}}

        result = await ParkingLotViewApi.get_view(int(lot_id))

        if result is not None:
            dict_result = dict(result)
            response_data["heat_map"] = dict_result["heat_map_data"]

        return create_success_response(response_data)

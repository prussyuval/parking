from aiohttp.web_response import Response

from apis.lot import LotApi
from rest_server.resources import CorsFixedResource
from rest_server.rest_utils import create_success_response


class LotResource(CorsFixedResource):
    async def get(self) -> Response:
        phrase = self.request.query.get('phrase')
        results = await LotApi.search_lot(phrase)

        return create_success_response(data=dict(options=[{result["eng_name"]: result["heb_name"]} for result in results]))

from aiohttp.web_response import Response

from rest_server.resources import CorsFixedResource
from rest_server.rest_utils import create_success_response


class OnlineResource(CorsFixedResource):
    async def get(self) -> Response:
        return create_success_response(data=dict(is_online=True))

    async def post(self) -> Response:
        return create_success_response(data=dict(is_online=True))

from rest_server.resources.online import OnlineResource
from rest_server.resources.status import StatusResource

API_PREFIX = '/api'


def attach_resources(cors, app) -> None:
    cors.add(app.router.add_route('GET', f'{API_PREFIX}/', OnlineResource))

    cors.add(app.router.add_route('*', f'{API_PREFIX}/status', LoginResource))

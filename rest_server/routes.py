from rest_server.resources.lot import LotResource
from rest_server.resources.online import OnlineResource
from rest_server.resources.status import StatusResource, PredictStatusResource

API_PREFIX = '/api'


def attach_resources(cors, app) -> None:
    cors.add(app.router.add_route('GET', f'{API_PREFIX}/', OnlineResource))

    cors.add(app.router.add_route('*', f'{API_PREFIX}/status', StatusResource))
    cors.add(app.router.add_route('*', f'{API_PREFIX}/predict-status', PredictStatusResource))
    cors.add(app.router.add_route('*', f'{API_PREFIX}/lot-search', LotResource))

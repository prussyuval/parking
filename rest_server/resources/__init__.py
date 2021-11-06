from aiohttp_cors import CorsViewMixin
from aiohttp.web import View


class CorsFixedResource(View, CorsViewMixin):
    pass

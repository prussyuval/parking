import asyncio

from aiohttp import web
import aiohttp_cors

from rest_server.routes import attach_resources
from utils.logging import logger
from utils.settings import REST_PORT

SESSION_COOKIE_NAME = 'session'


def initalize_cors(app):
    logger.debug("Initiate app with cors plugin")
    cors = aiohttp_cors.setup(app, defaults={
        '*': aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers='*',
            allow_methods='*',
            allow_headers='*',
        ),
    })
    attach_resources(cors, app)


async def get_app():
    app = web.Application()
    initalize_cors(app)
    return app


def main():
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(get_app())

    logger.info('Starting the rest server.')
    web.run_app(app, host='0.0.0.0', port=REST_PORT, access_log=logger,
                access_log_format='%a %t "%r" %s %b "%{Referer}i"')


if __name__ == '__main__':
    main()
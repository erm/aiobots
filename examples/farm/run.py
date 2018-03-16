from aiohttp import web
import aiobots
import settings

webapp = web.Application()
aiobots.setup(webapp, settings)
web.run_app(webapp, host=settings.HOSTNAME, port=settings.PORT)

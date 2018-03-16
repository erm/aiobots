import os

from aiohttp import web
import aiohttp_jinja2
import jinja2

from .helpers import get_reverse_match


class Bot:

    name = None
    data = {}

    def __init__(self, group):
        self.group = group

    # TODO: Helpers and raise if handle_response undefined


class BotView(web.View):

    app_name = None
    bots = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.webapp = self._request.app
        self.socket_groups = self.webapp['AIOBOTS']['APPS'][self.app_name]['socket_groups']
        self.group_name = self._request._match_info['group_name']
        aiohttp_jinja2.setup(
            self.webapp,
            loader=jinja2.FileSystemLoader(
                os.path.join(self.webapp['AIOBOTS']['SETTINGS'].APPS_DIR, 'templates')
            )
        )
        self.socket_groups[self.group_name] = {'bots': {}, 'data': {}, 'sockets': []}
        self.group = self.socket_groups[self.group_name]
        self.init_bots()

    def init_bots(self):
        bots = {bot.name: bot(self.group) for bot in self.bots}
        self.group['bots'] = bots

    async def __handle_request(self, method):
        request_path = self._request._rel_url.path
        match_info = self._request._match_info
        lookup_path = get_reverse_match(match_info) if match_info else request_path
        view = self.router.routes[lookup_path]
        if method not in view['methods']:
            raise web.HTTPMethodNotAllowed
        handler = view['func']
        response = await handler(self, self._request)
        return response

    async def get(self):
        return await self.__handle_request('GET')

    async def post(self):
        return await self.__handle_request('POST')

    async def get_response(self):
        response = web.WebSocketResponse()
        await response.prepare(self._request)
        self.group['sockets'].append(response)
        return response

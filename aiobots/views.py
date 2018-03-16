import os

from aiohttp import web
import aiohttp_jinja2
import jinja2


def get_reverse_match(match_info):
    return match_info._route._resource._formatter


class BotView(web.View):

    name = None
    botapp = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.webapp = self._request.app
        self.group_name = self._request._match_info['group_name']
        aiohttp_jinja2.setup(
            self.webapp,
            loader=jinja2.FileSystemLoader(
                os.path.join(self.webapp['AIOBOTS']['SETTINGS'].APPS_DIR, 'templates')
            )
        )
        self.webapp['AIOBOTS']['BOTS'][self.group_name] = []
        self.group = self.webapp['AIOBOTS']['BOTS'][self.group_name]

    async def __handle_request(self, method):
        request_path = self._request._rel_url.path
        match_info = self._request._match_info
        lookup_path = get_reverse_match(match_info) if match_info else request_path
        print(lookup_path)
        view = self.botapp.router[lookup_path]
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
        self.group.append(response)
        return response

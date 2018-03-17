import os

import aiohttp
from aiohttp import web
from aiohttp_session import get_session
import aiohttp_jinja2
import jinja2

from .helpers import get_reverse_match
from .sessions import get_identity


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
        self.socket_groups[self.group_name] = {'bots': {}, 'data': {'messages': []}, 'sessions': {}}
        self.group = self.socket_groups[self.group_name]
        self.sessions = self.group['sessions']
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
        session = await get_session(self._request)
        response = await handler(self, self._request, session)
        return response

    async def get(self):
        return await self.__handle_request('GET')

    async def post(self):
        return await self.__handle_request('POST')

    async def handle_ws(self):
        ws = web.WebSocketResponse()
        await ws.prepare(self._request)
        session = await get_session(self._request)
        identity = await get_identity(session)
        try:
            user = self.sessions[identity]
        except KeyError:
            self.sessions[identity] = {'sockets': []}
            user = self.sessions[identity]
            user['sockets'].append(ws)
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                if msg.data == 'close':
                    identity = await get_identity(session)
                    user = self.sessions[identity]
                    user['sockets'].remove(ws)
                    await ws.close()
                else:
                    msg_text = msg.data
                    group_msg = {'user': user, 'text': msg_text}
                    self.group['data']['messages'].append(group_msg)
                    for user in self.group['sessions']:
                        user_sockets = self.group['sessions'][user]['sockets']
                        for ws in user_sockets:
                            await ws.send_str(msg_text)
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print('Websocket connection closed with exception {}'.format(ws.exception()))
        return ws

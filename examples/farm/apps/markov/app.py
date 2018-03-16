# class WebsocketBot:

#     def __init__(self, ws_group):
#         self.ws_group = ws_group
#         self.data = {}

#     async def handle_msg(self, msg_data):
#         data = msg_data.split()
#         print(data)
#         for ws in self.ws_group['sockets']:
#             msg_resp = 'lol'
#             await ws.send_str(msg_resp)

from aiohttp import web
from aiohttp_jinja2 import render_template

from aiobots.views import BotView
from aiobots.apps import BotApp
from aiobots.helpers import get_url


botapp = BotApp()


class Markov(BotView):

    name = 'markov'
    botapp = botapp

    @botapp.route('/test/ws/{group_name}/', name='test_ws')
    async def ws_handler(self, *args, **kwargs):
        response = await self.get_response()
        async for msg in response:
            if msg.type == web.WSMsgType.TEXT:
                msg_data = msg.data
                for ws in self.group:
                    await ws.send_str(msg_data)
        return response

    @botapp.route('/test/{group_name}/', name='test')
    async def room(self, request, *args, **kwargs):
        ws_url = get_url(request, 'test_ws', kwargs={'group_name': self.group_name}, is_ws=True)
        context = {'ws_url': ws_url}
        return render_template('chat.html', request, context)


botapp.view_class = Markov

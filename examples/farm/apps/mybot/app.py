from aiohttp import web
from aiohttp_jinja2 import render_template

from aiobots.views import BotView, Bot
from aiobots.apps import BotApp, BotRouter
from aiobots.helpers import get_url


botapp = BotApp(app_name='mybot')


class MyBot(Bot):

    name = 'MyBot'

    async def handle_response(self, response):
        async for msg in response:
            if msg.type == web.WSMsgType.TEXT:
                msg_data = msg.data
                # conditions ...
                reply = 'Bot reply'
                for ws in self.group['sockets']:
                    await ws.send_str(reply)


class MyOtherBot(Bot):

    name = 'MyOtherBot'

    # async def handle_response(self, response):
    #     async for msg in response:
    #         if msg.type == web.WSMsgType.TEXT:
    #             msg_data = msg.data
    #             # conditions ...
    #             reply = 'Bot reply 2'
    #             for ws in self.group['sockets']:
    #                 await ws.send_str(reply)


class MyBotView(BotView):

    router = BotRouter()

    @router.route('/mybot/ws/{group_name}/', name='mybot_ws')
    async def ws_handler(self, *args, **kwargs):
        response = await self.get_response()
        async for msg in response:
            if msg.type == web.WSMsgType.TEXT:
                msg_data = msg.data
                for ws in self.group['sockets']:
                    await ws.send_str(msg_data)
        return response

    @router.route('/mybot/{group_name}/', name='mybot')
    async def room(self, request, *args, **kwargs):
        ws_url = get_url(request, 'mybot_ws', kwargs={'group_name': self.group_name}, is_ws=True)
        context = {'ws_url': ws_url}
        return render_template('chat.html', request, context)


botapp.register(MyBotView, bots=[MyBot, MyOtherBot])

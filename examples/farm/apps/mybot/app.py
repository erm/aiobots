from aiohttp import web
from aiohttp_jinja2 import render_template

from aiobots.views import BotView, Bot
from aiobots.apps import BotApp, BotRouter
from aiobots.helpers import get_url


botapp = BotApp(app_name='mybot')


class MyTestBot:

    name = None
    data = {}

    def __init__(self, group):
        self.group = group


class MyBotView(BotView):

    router = BotRouter()

    @router.route('/mybot/ws/{group_name}/', name='mybot_ws')
    async def ws_handler(self, request, session, *args, **kwargs):
        ws = await self.handle_ws()
        print('yes')
        print(ws)
        # TODO: Maybe just eliminate the need for an explicit handler? Not sure
        return ws

    @router.route('/mybot/{group_name}/', name='mybot')
    async def room(self, request, session, *args, **kwargs):
        ws_url = get_url(request, 'mybot_ws', kwargs={'group_name': self.group_name}, is_ws=True)
        context = {'ws_url': ws_url}
        return render_template('chat.html', request, context)


botapp.register(MyBotView, bots=[MyTestBot])

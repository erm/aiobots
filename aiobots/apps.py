class BotApp:

    routes = {}

    def __init__(self, app_name):
        self.app_name = app_name

    def register(self, view_class, bots=[]):
        view_class.bots = bots
        view_class.app_name = self.app_name
        self.routes[view_class] = view_class.router

    def setup(self, webapp):
        for view_class, router in self.routes.items():
            for route, view in router.routes.items():
                webapp.router.add_view(route, view_class, name=view['name'])


class BotRouter:

    routes = {}

    def route(self, route, name=None, methods=['GET']):
        def _route(func):
            self.routes[route] = {'func': func, 'name': name, 'methods': methods}
            return func
        return _route

class BotApp:

    router = {}
    view_class = None

    def route(self, route, name=None, methods=['GET']):
        def _route(func):
            self.router[route] = {'func': func, 'name': name, 'methods': methods}
            return func
        return _route

    def setup(self, webapp):
        for route, view in self.router.items():
            print(route)
            print(view)
            webapp.router.add_view(route, self.view_class, name=view['name'])

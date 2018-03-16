import sys
from importlib import import_module
from pkgutil import walk_packages

# def register(webapp):
#     def wrapper(klass):
#         class BotView(klass):
#             def __init__(self, *args, **kwargs):
#                 self.webapp = webapp
#                 super(BotView, self).__init__(*args, **kwargs)
#         return BotView
#     return wrapper


def setup(webapp, settings):
    webapp['AIOBOTS'] = {'SETTINGS': settings, 'APPS': {}, 'BOTS': {}}
    for app_name in settings.APPS_REGISTRY:
        print(app_name)
        try:
            app_module = import_module('apps.{}'.format(app_name))
        except ImportError as e:
            # raise AppModuleImportError(e)
            print(e)
        webapp['AIOBOTS']['APPS'][app_name] = app_module
        app_module.app.botapp.setup(webapp)

        
        





# def get_app_modules(app_name):
#     app_module = sys.modules[app_name]
#     sub_modules = {}
#     for importer, name, is_pkg in walk_packages(app_module.__path__):
#         module_pkg = '{}.{}'.format(app_name, name)
#         try:
#             sub_module = import_module(module_pkg)
#             sub_modules[name] = sub_module
#         except ImportError as e:
#             #raise AppModuleImportError('{}: {}'.format(module_pkg, e))
#             print(e)
#     return [sub_modules.keys()]

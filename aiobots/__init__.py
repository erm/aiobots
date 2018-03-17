from importlib import import_module

import aiohttp_session



def setup(webapp, settings):
    webapp['AIOBOTS'] = {'SETTINGS': settings, 'APPS': {}}
    for app_name in settings.APPS_REGISTRY:
        try:
            app_module = import_module('apps.{}'.format(app_name))
        except ImportError as e:
            # raise AppModuleImportError(e)
            raise e
        webapp['AIOBOTS']['APPS'][app_name] = {'socket_groups': {}}
        app_module.app.botapp.setup(webapp)
    aiohttp_session.setup(webapp, settings.SESSION_STORAGE)

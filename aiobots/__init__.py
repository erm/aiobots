from importlib import import_module


def setup(webapp, settings):
    webapp['AIOBOTS'] = {'SETTINGS': settings, 'APPS': {}}
    for app_name in settings.APPS_REGISTRY:
        try:
            app_module = import_module('apps.{}'.format(app_name))
        except ImportError as e:
            # raise AppModuleImportError(e)
            print(e)
        webapp['AIOBOTS']['APPS'][app_name] = {'socket_groups': {}}
        app_module.app.botapp.setup(webapp)

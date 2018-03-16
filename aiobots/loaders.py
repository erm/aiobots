import sys
from importlib import import_module
from pkgutil import walk_packages


def get_app_modules(app_name):
    app_module = sys.modules[app_name]
    sub_modules = {}
    for importer, name, is_pkg in walk_packages(app_module.__path__):
        module_pkg = '{}.{}'.format(app_name, name)
        try:
            sub_module = import_module(module_pkg)
            sub_modules[name] = sub_module
        except ImportError as e:
            # raise AppModuleImportError('{}: {}'.format(module_pkg, e))
            print(e)
    return [sub_modules.keys()]

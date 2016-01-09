import importlib

from django.apps import AppConfig, apps


class ShortcodesConfig(AppConfig):
    name = 'shortcodes'

    def ready(self):
        for app in apps.get_app_configs():
            importlib.import_module(app.name)
            try:
                importlib.import_module('.'.join([app.name, 'shortcodes']))
            except ImportError:
                pass

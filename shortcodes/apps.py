import importlib

from django.apps import AppConfig, apps


class ShortcodesConfig(AppConfig):
    name = 'shortcodes'

    def ready(self):
        # Register signals.
        from . import signals

        # Try importing "shortcodes" module from all apps.
        for app in apps.get_app_configs():
            importlib.import_module(app.name)
            try:
                importlib.import_module('.'.join([app.name, 'shortcodes']))
            except ImportError:
                pass

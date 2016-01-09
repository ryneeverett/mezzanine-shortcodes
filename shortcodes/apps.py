import sys
import importlib

from django.apps import AppConfig, apps
from django.conf import settings


class ShortcodesConfig(AppConfig):
    name = 'shortcodes'

    def ready(self):
        for app in apps.get_app_configs():
            importlib.import_module(app.name)
            try:
                importlib.import_module('.'.join([app.name, 'shortcodes']))
            except ImportError:
                pass

        if settings.DEBUG:
            from django.contrib.sites.models import Site

            try:
                addrport = sys.argv[-1] if sys.argv[-1] > 1024 else 8000
            except TypeError:
                addrport = 8000

            site = Site.objects.get_current()
            site.domain = '127.0.0.1:{port}'.format(port=addrport)
            site.save()

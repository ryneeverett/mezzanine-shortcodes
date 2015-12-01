#!/usr/bin/env python
import os
import sys
from django.db.utils import OperationalError

if __name__ == "__main__":

    from mezzanine.utils.conf import real_project_name

    settings_module = "%s.dev_settings" % real_project_name("project")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

    #  Set sites framework's domain for mezzanine-shortcodes.
    from django.contrib.sites.models import Site  # noqa

    try:
        addrport = sys.argv[-1] if sys.argv[-1] > 1024 else 8000
    except TypeError:
        addrport = 8000

    try:
        site = Site.objects.get_current()
    except OperationalError:  # Database hasn't been created yet.
        pass
    else:
        site.domain = '127.0.0.1:{port}'.format(port=addrport)
        site.save()

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

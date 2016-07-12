from mezzanine.core import forms
from django.contrib.sites.models import Site
from django.db.utils import OperationalError, ProgrammingError
try:
    DOMAIN = Site.objects.get_current().domain
except (OperationalError,   # Database doesn't exist.
        ProgrammingError):  # Database hasn't been initialized yet.
    DOMAIN = ''


class TinyMceWidget(forms.TinyMceWidget):
    class Media:
        extend = True
        js = (
            'shortcodes/tinymce/plugin.js',
            'http://' + DOMAIN + '/shortcodes/metadata.js'
        )

from mezzanine.core import forms
from django.contrib.sites.models import Site

DOMAIN = Site.objects.get_current().domain


class TinyMceWidget(forms.TinyMceWidget):
    class Media:
        extend = True
        js = (
            'shortcodes/tinymce/plugin.js',
            'http://' + DOMAIN + '/shortcodes/metadata.js'
        )

from mezzanine.core import forms


class TinyMceWidget(forms.TinyMceWidget):
    class Media:
        extend = True
        js = (
            'shortcodes/tinymce/plugin.js',
            '/shortcodes/metadata.js'
        )

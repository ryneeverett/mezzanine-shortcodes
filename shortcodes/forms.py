from mezzanine.core import forms

from .utils import ShortcodeSoup


class TinyMceWidget(forms.TinyMceWidget):
    class Media:
        extend = True
        js = (
            'shortcodes/tinymce/plugin.js',
            '/shortcodes/metadata.js'
        )

    def render(self, name, value, **kwargs):
        """ Display in admin. """
        if value:  # Initial value is None.
            value = ShortcodeSoup(value).render_admin_shortcodes()

        return super(TinyMceWidget, self).render(name, value, **kwargs)

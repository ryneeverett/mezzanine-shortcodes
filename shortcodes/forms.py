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

    def value_from_datadict(self, data, files, name):
        """ Clean up before saving. """
        dom = ShortcodeSoup(data[name])

        # Remove placeholders. If the parent element is otherwise empty, remove
        # it too.
        for tag in dom.find_all(
                'br', class_='mezzanine-shortcodes-placeholder'):
            if tag.previous_siblings or tag.next_siblings:
                tag.decompose()
            else:
                tag.parent.decompose()

        # Remove admin display.
        for tag in dom.find_shortcodes():
            del tag['style']
            tag.clear()

        data[name] = str(dom)
        return super(TinyMceWidget, self).value_from_datadict(
            data, files, name)

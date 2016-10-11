from bs4 import BeautifulSoup

from .register import Shortcode


class ShortcodeSoup(BeautifulSoup):
    def __init__(self, content):
        return super(ShortcodeSoup, self).__init__(content, 'html.parser')

    def find_shortcodes(self):
        return self.find_all('div', class_='mezzanine-shortcodes')

    def render_admin_shortcodes(self):
        """ Render shortcode tags to be displayed in the admin. """
        for tag in self.find_shortcodes():
            shortcode = Shortcode.from_func(tag.get('data-name'))

            if shortcode.iconurl:
                tag['style'] = "background-image: url({icon});".format(
                    icon=shortcode.iconurl)
            else:
                tag.string = shortcode.displayname

            tag['contenteditable'] = 'false'

            cursor_placeholder_content = self.new_tag('br')
            cursor_placeholder_content['class'] = (
                'mezzanine-shortcodes-placeholder')
            tag.insert_after(cursor_placeholder_content)

            # Tinymce would wrap our <br> in <p>'s anyway, so make it explicit.
            cursor_placeholder_content.wrap(self.new_tag('p'))

        return str(self)

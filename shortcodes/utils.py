from bs4 import BeautifulSoup


class ShortcodeSoup(BeautifulSoup):
    def __init__(self, content):
        return super(ShortcodeSoup, self).__init__(content, 'html.parser')

    def find_shortcodes(self):
        return self.find_all('div', class_='mezzanine-shortcodes')

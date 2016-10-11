import warnings
from django.conf import settings

from .register import Shortcode
from .utils import ShortcodeSoup


def getcontent(func, pk):
    shortcode = Shortcode.from_func(func)
    if settings.DEBUG:  # XXX Workaround for #8.
        try:
            instance = shortcode.get_instance(pk=pk)
        except shortcode.model.DoesNotExist as e:
            warnings.warn(str(e))
            return ''
    else:
        instance = shortcode.get_instance(pk=pk)
    return shortcode.fn(instance)


def richtext_filters(html):
    dom = ShortcodeSoup(html)

    for tag in dom.find_shortcodes():
        try:
            content = getcontent(tag.get('data-name'), tag.get('data-pk'))
        except Exception as e:
            if settings.DEBUG:
                raise
            else:
                content = ''
                warnings.warn(str(e))
        tag.replace_with(ShortcodeSoup(content))

    # BeautifulSoup adds closing br tags, which the browser interprets as
    # additional tags.
    return str(dom).replace("</br>", "")

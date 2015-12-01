import warnings
from django.conf import settings
from bs4 import BeautifulSoup
from . import state


def getcontent(func, pk):
    try:
        shortcode = state.SHORTCODES[func]
    except KeyError:
        raise KeyError(
            "Attempted to call nonexistant shortcode '{func}'.".format(
                func=func))

    model = shortcode.modelform._meta.model

    try:
        instance = model.objects.get(pk=pk)
    except model.DoesNotExist:
        raise model.DoesNotExist(
            "Model {model} instance {pk} does not exist.".format(
                model=model, pk=pk))

    return shortcode.fn(instance)


def richtext_filters(html):
    dom = BeautifulSoup(html, 'html.parser')

    for tag in dom.find_all('div', class_='mezzanine-shortcodes'):
        try:
            content = getcontent(tag.get('data-name'), tag.get('data-pk'))
        except Exception as e:
            if settings.DEBUG:
                raise
            else:
                content = ''
                warnings.warn(str(e))
        tag.replace_with(BeautifulSoup(content, 'html.parser'))

    return str(dom)

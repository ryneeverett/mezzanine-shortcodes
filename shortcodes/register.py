import textwrap
import warnings
import collections

from django.conf import settings
from django.contrib.staticfiles.templatetags import staticfiles

from mezzanine.utils.models import LazyModelOperations

from . import state, utils

lazy_model_ops = LazyModelOperations()


class Shortcode(object):
    def __init__(self, name, fn, modelform, **kwargs):
        """ Prepare metadata and register function. """
        self.name = name
        self.fn = fn
        self.modelform = modelform
        self.tooltip = kwargs.get('tooltip')

        icon = kwargs.get('icon')
        self.iconurl = staticfiles.static(icon) if icon else icon

        lazy_model_ops.add(self._post_model_load_hook, modelform._meta.model)

        if settings.DEBUG and self.name in state.SHORTCODES:
            warnings.warn("'{name}' was shadowed!".format(name=self.name))

        state.SHORTCODES[self.name] = self

    def _post_model_load_hook(self, model):
        self.displayname = model._meta.verbose_name

        # Display names must be unique.
        if settings.DEBUG:
            if self.displayname in state.DEBUG_DISPLAYNAMES:
                warnings.warn(textwrap.dedent("""
                    '{displayname}' is not a unique verbose_name!
                    Did you reuse model '{model}'?""".format(
                        displayname=self.displayname,
                        model=self.modelform._meta.model._meta.object_name)
                ))
            state.DEBUG_DISPLAYNAMES.add(self.displayname)


class Button(Shortcode):
    buttontype = 'button'

    def __init__(self, *args,  **kwargs):
        state.TOOLBAR.append(self)
        super().__init__(*args, **kwargs)


class MenuType(type):
    _buttons = collections.deque()  # [(fn, kwargs), ...]

    def __new__(cls, name, bases, classdict):
        """ Register a menu on definition. """
        package = classdict['__module__'].split('.')[0]
        klass = super(MenuType, cls).__new__(cls, name, bases, classdict)

        # Don't instantiate Menu itself, only subclasses.
        if package != 'shortcodes':

            klass.name = name
            klass.displayname = classdict.get('displayname', name)

            button_attrs = ['name', 'displayname', 'iconurl']
            klass.buttons = [{k: getattr(button, k) for k in button_attrs}
                             for button in cls.buttons]

            state.TOOLBAR.append(klass)

        return klass

    @classmethod
    def createButton(cls, *args, **kwargs):
        cls._buttons.append(Shortcode(*args, **kwargs))

    @utils.classproperty
    def buttons(cls):
        while cls._buttons:
            yield cls._buttons.popleft()

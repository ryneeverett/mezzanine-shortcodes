import inspect
import textwrap
import warnings

from django.conf import settings
from django.contrib.staticfiles.templatetags import staticfiles

from . import state


class Shortcode(object):
    def __init__(self, name, fn, modelform, **kwargs):
        """ Prepare metadata and register function. """
        self.name = name
        self.fn = fn
        self.modelform = modelform
        self.tooltip = kwargs.get('tooltip')
        self.displayname = modelform._meta.model._meta.verbose_name

        icon = kwargs.get('icon')
        self.iconurl = staticfiles.static(icon) if icon else icon

        if settings.DEBUG:
            # Display names must be unique.
            if self.displayname in state.DEBUG_DISPLAYNAMES:
                self.warn("""
                '{displayname}' is not a unique verbose_name!
                Did you reuse model '{model}'?""".format(
                    displayname=self.displayname,
                    model=self.modelform._meta.model._meta.object_name)
                )
            else:
                state.DEBUG_DISPLAYNAMES.add(self.displayname)

            # Probably don't want to shadow names either.
            if self.name in state.SHORTCODES:
                warnings.warn("'{name}' was shadowed!".format(name=self.name))

        state.SHORTCODES[self.name] = self

    def warn(self, msg):
        warnings.warn_explicit(
            textwrap.dedent(msg), UserWarning,
            filename=inspect.getfile(self.fn),
            lineno=inspect.getsourcelines(self.fn)[1])


class Button(Shortcode):
    buttontype = 'button'

    def __init__(self, *args,  **kwargs):
        state.TOOLBAR.append(self)
        super().__init__(*args, **kwargs)


class MenuType(type):
    buttons = []  # [(fn, kwargs), ...]

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
            cls.buttons.clear()

            state.TOOLBAR.append(klass)

        return klass

    @classmethod
    def createButton(cls, *args, **kwargs):
        cls.buttons.append(Shortcode(*args, **kwargs))

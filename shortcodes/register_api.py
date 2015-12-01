from django.forms import model_to_dict
from django.template.loader import render_to_string

from . import register


class Menu(object, metaclass=register.MenuType):
    buttontype = 'menubutton'


def button(modelform, **kwargs):
    def wrapper(fn):
        register.Button(fn.__name__, fn, modelform, **kwargs)
        return fn
    return wrapper


def menubutton(modelform, **kwargs):
    def wrapper(fn):
        register.MenuType.createButton(fn.__name__, fn, modelform, **kwargs)
        return fn
    return wrapper


def generic_shortcode_factory(template):
    def generic_shortcode(instance):
        return render_to_string(template, context=model_to_dict(instance))
    return generic_shortcode


def GenericButton(name, modelform, template, **kwargs):
    register.Button(
        name, generic_shortcode_factory(template), modelform, **kwargs)


def GenericMenubutton(name, modelform, template, **kwargs):
    register.MenuType.createButton(
        name, generic_shortcode_factory(template), modelform, **kwargs)

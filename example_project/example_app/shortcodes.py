from django.forms import model_to_dict
from django.template.loader import render_to_string
import shortcodes
from . import models


@shortcodes.button(models.FeaturefulButtonForm, tooltip='Click me.')
def featureful_button(instance):
    prefix = instance.Prefix + ' ' if instance.Prefix else ''
    return '<p>Hello {prefix}{entity}!</p>'.format(
        prefix=prefix, entity=instance.entity)


@shortcodes.button(models.SomeButtonForm, icon='img/audio.png')
def icon_button(instance):
    return render_to_string('person.html', context=model_to_dict(instance))


shortcodes.GenericButton(
    'my_generic_button', models.GenericButtonForm, 'person.html')


class SomeMenu(shortcodes.Menu):
    tooltip = 'Click here.'
    displayname = 'Some Menu'

    @shortcodes.menubutton(models.SomeMenubuttonForm)
    def some_menubutton():
        pass

    @shortcodes.menubutton(models.IconMenubutton, icon='img/audio.png')
    def icon_menubutton():
        pass

    shortcodes.GenericMenubutton(
        'generic_menubutton', models.GenericMenubuttonForm, 'person.html')

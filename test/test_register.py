import importlib
from unittest import mock

from django import forms
from django.db import models
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

import testbase
import testutils

try:
    hasattr(settings, 'DEBUG')
except ImproperlyConfigured:
    pass
else:
    from shortcodes import state, register, register_api


class TestShortcodeBase(testbase.ShortcodesTestCase):
    @classmethod
    def setUpClass(cls):

        class _model(models.Model):
            class Meta:
                verbose_name = 'Model Name'
                app_label = 'test'

        class modelform(forms.ModelForm):
            class Meta:
                model = _model
                fields = '__all__'

        def shortcode(instance):
            pass

        cls.modelform = modelform
        cls.shortcode = shortcode


class TestShortcode(TestShortcodeBase):
    def makeShortcode(self):
        return register.Shortcode(
            self.shortcode.__name__, self.shortcode, self.modelform)

    def test_registration(self):
        sc = self.makeShortcode()

        self.assertEqual(sc.fn, self.shortcode)
        self.assertEqual(sc.name, self.shortcode.__name__)
        self.assertEqual(sc.modelform, self.modelform)
        self.assertFalse(sc.tooltip)
        self.assertFalse(sc.iconurl)
        self.assertEqual(sc.displayname, 'Model Name')

        self.assertIn(sc.name, state.SHORTCODES)

    def test_registration_featureshuge(self):
        sc = register.Shortcode(
            'lot-o-features',
            self.shortcode,
            self.modelform,
            tooltip='click',
            icon='file.ext')

        self.assertEqual(sc.fn, self.shortcode)
        self.assertEqual(sc.name, 'lot-o-features')
        self.assertEqual(sc.modelform, self.modelform)
        self.assertEqual(sc.tooltip, 'click')
        self.assertEqual(sc.iconurl, '/static/file.ext')
        self.assertEqual(sc.displayname, 'Model Name')

        self.assertIn(sc.name, state.SHORTCODES)

    @mock.patch('shortcodes.register.settings.DEBUG', True)
    def test_duplicatefunc_dev(self):
        """ Name must be unique. """
        self.makeShortcode()
        with self.assertWarnsRegex(UserWarning, 'shadow'):
            self.makeShortcode()

    @mock.patch('shortcodes.register.settings.DEBUG', True)
    def test_duplicatedisplayname_dev(self):
        """ Displayname must be unique. """
        self.makeShortcode()
        with self.assertWarnsRegex(UserWarning, 'verbose_name'):
            self.makeShortcode()

    @mock.patch('shortcodes.register.settings.DEBUG', False)
    def test_duplicate_prod(self):
        """ Don't check for duplicates in production. """
        self.makeShortcode()
        with self.assertRaises(AssertionError):
            with self.assertWarns(UserWarning):
                self.makeShortcode()


class TestButton(TestShortcodeBase):
    def test_registration(self):
        button = register.Button(
            self.shortcode.__name__, self.shortcode, self.modelform)

        self.assertEqual(button.buttontype, 'button')
        self.assertIn(button, state.TOOLBAR)

    def test_api(self):

        @register_api.button(self.modelform, tooltip='Click me.', icon='file.ext')
        def some_button(instance):
            pass

        some_button_obj = state.TOOLBAR.pop()
        self.assertEqual(some_button_obj.name, some_button.__name__)
        self.assertEqual(some_button_obj.modelform, self.modelform)
        self.assertEqual(some_button_obj.tooltip, 'Click me.')
        self.assertEqual(some_button_obj.iconurl, '/static/file.ext')


class TestMenu(TestShortcodeBase):
    def test_instantiation(self):

        class SomeMenu(register_api.Menu):
            displayname = "Any Ole' Menu"

        self.assertEqual(SomeMenu.buttontype, 'menubutton')
        self.assertEqual(SomeMenu.name, SomeMenu.__name__)
        self.assertEqual(SomeMenu.displayname, "Any Ole' Menu")
        self.assertEqual(SomeMenu.buttons, [])

        self.assertIn(SomeMenu, state.TOOLBAR)

    def test_api(self):

        class SomeMenu(register_api.Menu):
            displayname = "Any Ole' Menu"
            tooltip = 'Click me.'

            @register_api.menubutton(self.modelform, icon='file.ext')
            def some_menubutton(instance):
                pass

            register_api.GenericMenubutton(
                'some_button', self.modelform, 'template.html')

        self.assertEqual(SomeMenu.name, SomeMenu.__name__)
        self.assertEqual(SomeMenu.displayname, "Any Ole' Menu")
        self.assertEqual(SomeMenu.tooltip, 'Click me.')

        self.assertEqual(SomeMenu.buttons, [
            {'name': SomeMenu.some_menubutton.__name__,
             'displayname': self.modelform._meta.model._meta.verbose_name,
             'iconurl': '/static/file.ext'},
            {'name': 'some_button',
             'displayname': self.modelform._meta.model._meta.verbose_name,
             'iconurl': None}
        ])

        self.assertIn(SomeMenu, state.TOOLBAR)

    def test_menu_baseclass_not_in_toolbar(self):
        """ Menu base class should not be added to toolbar. """
        importlib.reload(register_api)
        self.assertFalse(state.TOOLBAR)


class TestGenericButton(TestShortcodeBase):
    def test_api(self):
        register_api.GenericButton(
            'some_button', self.modelform, 'template.html')

        some_button_obj = state.TOOLBAR.pop()
        self.assertEqual(some_button_obj.name, 'some_button')
        self.assertEqual(some_button_obj.modelform, self.modelform)
        self.assertEqual(some_button_obj.fn.__name__, 'generic_shortcode')


if __name__ == '__main__':
    testutils.test_module('test_register')

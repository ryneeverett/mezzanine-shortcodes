from unittest import mock

from django.conf import settings
from django.test import TestCase
from django.core.exceptions import ImproperlyConfigured

import testutils

try:
    hasattr(settings, 'DEBUG')
except ImproperlyConfigured:
    pass
else:
    from shortcodes import state, render

PRE_HTML = """\
<p><strong>An example:</strong></p>
<div class='mezzanine-shortcodes' data-name='featureful_button' data-pk='{pk}'>
</div>
<p>That was it. Show's over folks.</p>
"""
POST_HTML = """\
<p><strong>An example:</strong></p>
{content}
<p>That was it. Show's over folks.</p>
"""


class TestFilters(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.model = state.SHORTCODES['featureful_button'].modelform._meta.model
        cls.model(entity='Stanley').save()

    def test_richtext_filters(self):
        result = render.richtext_filters(PRE_HTML.format(pk=1))
        expected_result = POST_HTML.format(content='<p>Hello Stanley!</p>')
        self.assertEqual(result, expected_result)

    @mock.patch('shortcodes.render.settings.DEBUG', True)
    def test_richtext_filters_error_dev(self):
        with self.assertRaisesRegex(self.model.DoesNotExist, 'does not exist'):
            render.richtext_filters(PRE_HTML.format(pk=100))

    def test_richtext_filters_error_prod(self):
        with self.assertWarnsRegex(UserWarning, 'does not exist'):
            result = render.richtext_filters(PRE_HTML.format(pk=100))
        expected_result = POST_HTML.format(content='')
        self.assertEqual(result, expected_result)

    def test_getcontent(self):
        content = render.getcontent('featureful_button', 1)
        self.assertEqual(content, '<p>Hello Stanley!</p>')

    def test_getcontent_nonexistantshortcode(self):
        with self.assertRaisesRegex(KeyError, 'nonexistant shortcode'):
            render.getcontent('imaginary_button', 1)

    def test_getcontent_nonexistantmodelinstance(self):
        with self.assertRaisesRegex(self.model.DoesNotExist, 'does not exist'):
            render.getcontent('featureful_button', 100)


if __name__ == '__main__':
    testutils.test_module('test_render')

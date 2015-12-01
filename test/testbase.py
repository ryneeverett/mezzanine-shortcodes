import unittest
import importlib

# Since shortcodes accesses django settings, they must be configured before
# importing shortcodes, so testbase must always be imported before shortcodes.
from django.conf import settings
try:
    settings.configure(STATIC_URL='/static/')
except RuntimeError:
    pass  # Settings already configured.

import shortcodes.state


class ShortcodesTestCase(unittest.TestCase):

    def tearDown(self):
        """ Reset module state. """
        importlib.reload(shortcodes.state)
        importlib.reload(shortcodes)

import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner


def run_module(*modules):
    sys.path.append(os.path.realpath('./example_project'))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'example_project.project.settings'
    django.setup()

    testrunner = get_runner(settings)()
    failures = testrunner.run_tests(modules)
    return bool(failures)


def test_module(*modules):
    is_failure = run_module(modules)
    sys.exit(is_failure)

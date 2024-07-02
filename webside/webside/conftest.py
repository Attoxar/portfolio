import os
import pytest
from django.conf import settings

def pytest_configure():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'webside.settings'
    settings.DEBUG = False
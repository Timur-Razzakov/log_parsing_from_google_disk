import pytest
from django.conf import settings


@pytest.fixture(autouse=True)
def use_test_database(settings):
    settings.DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }

#!/usr/bin/env python
import sys

import django
from django.conf import settings


if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=(
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'rapidsms',
            'rtwilio',
        ),
        SITE_ID=1,
        SECRET_KEY='super-secret',
        MIDDLEWARE_CLASSES=(
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ),
        ROOT_URLCONF='rtwilio.tests.urls',
        PASSWORD_HASHERS=(
            'django.contrib.auth.hashers.MD5PasswordHasher',
        ),
        LOGGING={
            'version': 1,
            'disable_existing_loggers': False,
            'handlers': {
                'null': {
                    'level': 'DEBUG',
                    'class': 'django.utils.log.NullHandler',
                },
            },
            'loggers': {
                'rapidsms': {
                    'handlers': ['null'],
                    'level': 'DEBUG',
                },
                'rtwilio': {
                    'handlers': ['null'],
                    'level': 'DEBUG',
                }
            }
        },
    )


from django.test.utils import get_runner


def runtests():
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True, failfast=False)
    failures = test_runner.run_tests(['rtwilio', ])
    sys.exit(failures)


if __name__ == '__main__':
    runtests()

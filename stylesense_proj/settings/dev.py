from .base import *
import subprocess

root_path = os.path.abspath(os.path.join(os.path.realpath(__file__), '..', '..', '..', '..'))

DEBUG = True

# *********** DATABASES ***********

localhost = '127.0.0.1'


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": '',
        "USER": '',
        "PASSWORD": '',
        "HOST": '',
        "PORT": ''
    }
}

ROOT_URLCONF = 'stylesense_proj.urls'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'verbose',
        },

        'console1': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'apps': {
            'handlers': ['console1'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'app': {
            'handlers': ['console1'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
    'formatters': {
        'verbose': {
            'format': log_format_brief
        },
        'simple': {
            'format': log_format
        },
    },
}
BROKER_URL = 'redis://localhost:6379'
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'

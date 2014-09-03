import os
from urlparse import urlsplit
url = os.getenv('MONGOHQ_URL', 'mongodb://localhost:27017/pupa')

# @see https://raw.github.com/opencivicdata/pupa/master/pupa/core/default_settings.py
MONGO_HOST = url
MONGO_PORT = 27017
MONGO_DATABASE = urlsplit(url).path[1:]

SCRAPELIB_RPM = 60
SCRAPELIB_TIMEOUT = 60
SCRAPELIB_RETRY_ATTEMPTS = 3
SCRAPELIB_RETRY_WAIT_SECONDS = 20

ENABLE_ELASTICSEARCH = False
ELASTICSEARCH_HOST = 'localhost'
ELASTICSEARCH_TIMEOUT = 2

BILL_FILTERS = {}
LEGISLATOR_FILTERS = {}
EVENT_FILTERS = {}

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': "%(asctime)s %(levelname)s %(name)s: %(message)s",
            'datefmt': '%H:%M:%S'
        }
    },
    'handlers': {
        'default': {'level': 'INFO',
                    'class': 'pupa.ext.ansistrm.ColorizingStreamHandler',
                    'formatter': 'standard'},
    },
    'loggers': {
        '': {
            'handlers': ['default'], 'level': 'WARN', 'propagate': True
        },
        'scrapelib': {
            'handlers': ['default'], 'level': 'WARN', 'propagate': False
        },
        'requests': {
            'handlers': ['default'], 'level': 'WARN', 'propagate': False
        },
        'boto': {
            'handlers': ['default'], 'level': 'WARN', 'propagate': False
        },
    },
}

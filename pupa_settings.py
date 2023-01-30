import os

# Use the same directories as scrapers_ca_app.
CACHE_DIR = os.path.join(os.getcwd(), "..", "_cache")
SCRAPED_DATA_DIR = os.path.join(os.getcwd(), "..", "_data")
DATABASE_URL = os.environ.get("DATABASE_URL", "postgis://root:root@localhost/pupa")
os.environ["OCD_DIVISION_CSV"] = os.environ.get(
    "OCD_DIVISION_CSV", os.path.join(os.path.abspath(os.path.dirname(__file__)), "country-{}.csv")
)

# @see https://github.com/opencivicdata/pupa/blob/master/pupa/settings.py
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"standard": {"format": "%(asctime)s %(levelname)s %(name)s: %(message)s", "datefmt": "%H:%M:%S"}},
    "handlers": {
        "default": {"level": "DEBUG", "class": "pupa.ext.ansistrm.ColorizingStreamHandler", "formatter": "standard"},
    },
    "loggers": {
        "": {"handlers": ["default"], "level": "DEBUG", "propagate": True},  # DEBUG
        "scrapelib": {"handlers": ["default"], "level": "INFO", "propagate": False},  # INFO
        "requests": {"handlers": ["default"], "level": "WARN", "propagate": False},
        "boto3": {"handlers": ["default"], "level": "WARN", "propagate": False},
    },
}

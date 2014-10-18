import os

# Use the same directories as scrapers_ca_app.
CACHE_DIR = os.path.join(os.getcwd(), '..', '_cache')
SCRAPED_DATA_DIR = os.path.join(os.getcwd(), '..', '_data')
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgis://localhost/pupa')
OCD_DIVISION_CSV = os.environ.get('OCD_DIVISION_CSV', os.path.join(os.path.abspath(os.path.dirname(__file__)), 'country-{}.csv'))

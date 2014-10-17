import os

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgis://localhost/pupa')
OCD_DIVISION_CSV = os.environ.get('OCD_DIVISION_CSV', os.path.join(os.path.abspath(os.path.dirname(__file__)), 'country-{}.csv'))

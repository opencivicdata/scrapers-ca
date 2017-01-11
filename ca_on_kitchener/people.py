from __future__ import unicode_literals
from utils import CSVScraper


class KitchenerPersonScraper(CSVScraper):
    csv_url = 'http://app.kitchener.ca/opendata/csv/Elected_Officials.csv'

from __future__ import unicode_literals
from utils import CSVScraper


class LondonPersonScraper(CSVScraper):
    csv_url = 'http://apps.london.ca/OpenData/CSV/Council.csv'

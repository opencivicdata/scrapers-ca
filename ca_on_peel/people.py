from __future__ import unicode_literals
from utils import CSVScraper

COUNCIL_PAGE = 'http://opendata.peelregion.ca/media/33531/wards1418_csv.csv'


class PeelPersonScraper(CSVScraper):
    csv_url = 'http://opendata.peelregion.ca/media/33531/wards1418_csv.csv'

from __future__ import unicode_literals
from utils import CSVScraper

COUNCIL_PAGE = 'http://opendata.peelregion.ca/media/25713/ward20102014_csv_12.2013.csv'


class PeelPersonScraper(CSVScraper):
    csv_url = 'http://opendata.peelregion.ca/media/33531/wards1418_csv.csv'

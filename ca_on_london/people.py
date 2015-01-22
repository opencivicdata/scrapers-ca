from __future__ import unicode_literals
from utils import CSVScraper

COUNCIL_PAGE = 'http://www.london.ca/city-hall/city-council/Pages/default.aspx'


class LondonPersonScraper(CSVScraper):
    csv_url = 'http://apps.london.ca/OpenData/CSV/Council.csv'

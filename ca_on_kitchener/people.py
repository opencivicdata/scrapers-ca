from __future__ import unicode_literals
from utils import CSVScraper

COUNCIL_PAGE = 'http://www.kitchener.ca/en/insidecityhall/WhoIsMyCouncillor.asp'


class KitchenerPersonScraper(CSVScraper):
    csv_url = 'http://app.kitchener.ca/opendata/csv/Elected_Officials.csv'

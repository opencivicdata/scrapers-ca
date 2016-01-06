from __future__ import unicode_literals
from utils import CSVScraper

COUNCIL_PAGE = 'http://www.greatersudbury.ca/inside-city-hall/city-council/'


class GreaterSudburyPersonScraper(CSVScraper):
    csv_url = 'http://opendata.greatersudbury.ca/datasets/cc23919fdcff4f5fa2290dbc01571df5_0.csv'
    header_converter = lambda self, s: s.lower().replace('_', ' ')

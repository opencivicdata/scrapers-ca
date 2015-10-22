from __future__ import unicode_literals
from utils import CSVScraper

COUNCIL_PAGE = 'http://www.oakville.ca/townhall/council.html'


class OakvillePersonScraper(CSVScraper):
    csv_url = 'http://opendata.oakville.ca/Oakville_Town_Council/Oakville_Town_Council.csv'
    encoding = 'windows-1252'
    header_converter = lambda self, s: s.lower().replace('Phone (cell)', 'Cell')
    corrections = {
      'primary role': {
        'Town Councillor': 'Councillor',
        'Regional and Town Councillor': 'Regional Councillor',
      },
    }

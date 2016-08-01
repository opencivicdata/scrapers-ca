from __future__ import unicode_literals
from utils import CSVScraper

COUNCIL_PAGE = 'http://www.countygp.ab.ca/EN/main/government/council.html'


class GrandePrairieCountyNo1PersonScraper(CSVScraper):
    csv_url = 'http://data.countygp.ab.ca/data/ElectedOfficials/elected-officials.csv'

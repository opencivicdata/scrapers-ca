from __future__ import unicode_literals
from utils import CSVScraper


class StrathconaCountyPersonScraper(CSVScraper):
    csv_url = 'https://data.strathcona.ca/api/views/suw8-zxcy/rows.csv?accessType=DOWNLOAD'

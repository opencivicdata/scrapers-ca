from __future__ import unicode_literals
from utils import CSVScraper

COUNCIL_PAGE = 'http://www.strathcona.ca/local-government/mayor-councillors/councillors/'


class StrathconaCountyPersonScraper(CSVScraper):
    csv_url = 'https://data.strathcona.ca/api/views/suw8-zxcy/rows.csv?accessType=DOWNLOAD'

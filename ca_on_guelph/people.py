from __future__ import unicode_literals
from utils import CSVScraper

COUNCIL_PAGE = 'http://guelph.ca/city-hall/mayor-and-council/city-council/'


class GuelphPersonScraper(CSVScraper):
    csv_url = 'http://open.guelph.ca/wp-content/uploads/2014/12/GuelphCityCouncil2014-2018ElectedOfficalsContactInformation.csv'

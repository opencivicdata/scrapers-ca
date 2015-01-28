from __future__ import unicode_literals
from utils import CSVScraper

COUNCIL_PAGE = 'http://www.victoria.ca/EN/main/city/mayor-council-committees/councillors.html'


class VictoriaPersonScraper(CSVScraper):
    csv_url = 'http://www.victoria.ca/assets/City~Hall/Open~Data/Councillor%20Contact%20Info.csv'
    many_posts_per_area = True

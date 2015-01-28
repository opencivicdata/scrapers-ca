from __future__ import unicode_literals
from utils import CSVScraper

COUNCIL_PAGE = 'http://www.kelowna.ca/CM/Page159.aspx'


class KelownaPersonScraper(CSVScraper):
    csv_url = 'http://www.kelowna.ca/images/opendata/CouncilContactInformation.csv'
    many_posts_per_area = True

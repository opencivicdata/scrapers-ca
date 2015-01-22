from __future__ import unicode_literals
from utils import CSVScraper

COUNCIL_PAGE = 'http://www.welland.ca/Council/index.asp'


class WellandPersonScraper(CSVScraper):
    csv_url = 'http://www.welland.ca/open/Datasheets/Welland_mayor_and_council_members.csv'
    encoding = 'windows-1252'
    many_posts_per_area = True

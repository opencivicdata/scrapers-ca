from __future__ import unicode_literals
from utils import CSVScraper

COUNCIL_PAGE = 'http://vancouver.ca/your-government/vancouver-city-council.aspx'


class VancouverPersonScraper(CSVScraper):
    csv_url = 'ftp://webftp.vancouver.ca/OpenData/csv/ElectedOfficialsContactInformation.csv'
    many_posts_per_area = True
    skip_rows = 1

from __future__ import unicode_literals
from utils import CSVScraper


class GrandePrairiePersonScraper(CSVScraper):
    csv_url = 'https://data.cityofgp.com/api/views/kxpv-69sa/rows.csv?accessType=DOWNLOAD'
    many_posts_per_area = True

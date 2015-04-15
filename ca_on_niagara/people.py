from __future__ import unicode_literals
from utils import CSVScraper

COUNCIL_PAGE = 'http://www.niagararegion.ca/test/sherpa-list-to-csv.aspx?list=council-elected-officials-csv'


class NiagaraPersonScraper(CSVScraper):
    csv_url = 'http://www.niagararegion.ca/test/sherpa-list-to-csv.aspx?list=council-elected-officials-csv'
    many_posts_per_area = True

from __future__ import unicode_literals
from utils import CSVScraper

COUNCIL_PAGE = 'http://www.tol.ca/About-the-Township/Municipal-Government/Mayor-and-Council'


class LangleyPersonScraper(CSVScraper):
    csv_url = 'https://data.tol.ca/api/views/ykn8-vbpf/rows.csv?accessType=DOWNLOAD'
    many_posts_per_area = True

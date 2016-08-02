from __future__ import unicode_literals
from utils import CSVScraper

COUNCIL_PAGE = 'http://lincoln.ca/content/mayor-and-council'


class LincolnPersonScraper(CSVScraper):
    csv_url = 'https://www.niagaraopendata.ca//dataset/a19ecca4-b128-4779-9c42-fddb5bd5d9e8/resource/f453db0b-ba02-43d1-9e46-d0e7065862e4/download/lincolncouncil20160303.csv'
    many_posts_per_area = True

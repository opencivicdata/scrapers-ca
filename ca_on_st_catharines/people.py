from __future__ import unicode_literals
from utils import CSVScraper

COUNCIL_PAGE = 'http://www.stcatharines.ca/en/governin/MayorCouncil.asp'


class StCatharinesPersonScraper(CSVScraper):
    csv_url = 'https://www.niagaraopendata.ca//dataset/ccb9c7f1-d3b0-4049-9c08-e4f7b048722c/resource/128a39f0-8234-4708-b69b-9c73f7a55475/download/stcathcounsilors.csv'
    many_posts_per_area = True

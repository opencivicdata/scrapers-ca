# coding: utf-8
from __future__ import unicode_literals
from utils import CSVScraper

COUNCIL_PAGE = 'http://ottawa.ca/en/city-council'


class OttawaPersonScraper(CSVScraper):
    csv_url = 'http://data.ottawa.ca/en/storage/f/2015-01-22T170049/Elected-Officials-%282014-2018%29-v.2.csv'

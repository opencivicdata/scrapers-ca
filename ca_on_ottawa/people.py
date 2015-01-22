# coding: utf-8
from __future__ import unicode_literals
from utils import CSVScraper

COUNCIL_PAGE = 'http://ottawa.ca/en/city-council'


class OttawaPersonScraper(CSVScraper):
    csv_url = 'http://data.ottawa.ca/storage/f/2014-12-09T215925/Elected-Officials-%282014-2018%29.csv'

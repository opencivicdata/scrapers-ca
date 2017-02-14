from __future__ import unicode_literals
from utils import CSVScraper


class KelownaPersonScraper(CSVScraper):
    csv_url = 'https://opendata.arcgis.com/datasets/9333b66380424479816685a9fe44f06f_0.csv'
    many_posts_per_area = True

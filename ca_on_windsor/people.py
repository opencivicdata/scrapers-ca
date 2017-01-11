from __future__ import unicode_literals
from utils import CSVScraper


class WindsorPersonScraper(CSVScraper):
    csv_url = 'http://www.citywindsor.ca/opendata/Lists/OpenData/Attachments/33/City%20Windsor%20Elected%20Officials.csv'

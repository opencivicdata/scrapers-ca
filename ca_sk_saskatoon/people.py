from __future__ import unicode_literals
from utils import CSVScraper


class SaskatoonPersonScraper(CSVScraper):
    # 2017-01-27: The CSV is not yet online, so we must manually upload a copy to S3.
    csv_url = 'http://represent.opennorth.ca.s3.amazonaws.com/data/2017-01-27-saskatoon.csv'

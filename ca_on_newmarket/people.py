from __future__ import unicode_literals
from utils import CSVScraper


class NewmarketPersonScraper(CSVScraper):
    # There's no permalink to the ZIP or CSV, so we must manually upload a copy to S3.
    # http://open.newmarket.ca/opendata/navigo/#/show/SQLQ6R6C_10?disp=D1579414319D
    csv_url = 'http://represent.opennorth.ca.s3.amazonaws.com/data/2016-11-15-newmarket.csv'
    corrections = {
        'primary role': {
            'Deputy Mayor and Regional Councillor': 'Deputy Mayor',
        },
    }
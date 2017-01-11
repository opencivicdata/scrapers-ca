from __future__ import unicode_literals
from utils import CSVScraper


class NewmarketPersonScraper(CSVScraper):
    # There's no permalink to the ZIP or CSV.
    # http://open.newmarket.ca/opendata/navigo/#/show/SQLQ6R6C_10?disp=D1579414319D
    csv_url = 'http://represent.opennorth.ca.s3.amazonaws.com/data/mayor_and_councillors_contact_information_2014_2018.csv'

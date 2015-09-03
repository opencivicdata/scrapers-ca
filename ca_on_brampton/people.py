from __future__ import unicode_literals
from utils import CSVScraper

COUNCIL_PAGE = 'http://www.brampton.ca/en/City-Hall/CouncilOffice/Pages/Welcome.aspx'


class BramptonPersonScraper(CSVScraper):
    csv_url = 'http://www.brampton.ca/EN/City-Hall/OpenGov/Open-Data-Catalogue/Documents/Brampton-Elected-Officials.csv'

from __future__ import unicode_literals
from utils import CSVScraper

COUNCIL_PAGE = 'http://www.burlington.ca/en/services-for-you/Council-Members-and-Wards.asp'


class BurlingtonPersonScraper(CSVScraper):
    csv_url = 'http://www.burlington.ca/en/services-for-you/resources/Ongoing_Projects/Open_Data/Catalogue/Feb_23_2015_Update/Elected_Official_Contact_PostedMar19.csv'

from __future__ import unicode_literals
from utils import CSVScraper

COUNCIL_PAGE = 'http://www.cityofkingston.ca/city-hall/city-council/mayor-and-council'


class KingstonPersonScraper(CSVScraper):
    csv_url = 'https://www.cityofkingston.ca/cok/data/council_Contacts/Council_Contact_List.csv'
    corrections = {
      'district name': {
        "King\u0092s Town": "King's Town",
      },
    }
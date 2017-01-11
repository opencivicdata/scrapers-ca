from __future__ import unicode_literals
from utils import CSVScraper


class KingstonPersonScraper(CSVScraper):
    csv_url = 'https://www.cityofkingston.ca/cok/data/council_Contacts/Council_Contact_List.csv'
    corrections = {
        'district name': {
            "King\u0092s Town": "King's Town",
        },
    }

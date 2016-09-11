from __future__ import unicode_literals
from utils import CSVScraper

COUNCIL_PAGE = 'http://www.saintjohn.ca/en/home/cityhall/mayor-and-council/councillors.aspx'


class SaintJohnPersonScraper(CSVScraper):
    csv_url = 'http://www.saintjohn.ca/site/media/SaintJohn/Saint_John_NB_Elected_Officials_Contact_Info.zip'
    filename = 'Saint_John_NB_Elected_Officials_Contact_Info.csv'
    many_posts_per_area = True
    corrections = {
        'district name': {
            'City of Saint John': 'Saint John',
        },
        'primary role': {
            'Deputy Mayor ': 'Councillor',  # varies
        },
    }

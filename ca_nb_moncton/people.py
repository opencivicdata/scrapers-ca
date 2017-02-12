from __future__ import unicode_literals
from utils import CSVScraper


class MonctonPersonScraper(CSVScraper):
    csv_url = 'http://www.moncton.ca/OpenData/Elected_Officials_Contact_Information-Coordonnes_des_elus.zip'
    encoding = 'windows-1252'
    filename = 'Elected Officials Contact Information.csv'
    many_posts_per_area = True

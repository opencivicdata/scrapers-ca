from __future__ import unicode_literals
from utils import CSVScraper

from datetime import date


class PeterboroughPersonScraper(CSVScraper):
    csv_url = 'https://docs.google.com/spreadsheets/d/146Ym9eJ624pHQLF0HAtoiCLfP2WyHVerla2rT1nbMsE/pub?gid=0&single=true&output=csv'
    many_posts_per_area = True
    created_at = date(2016, 3, 16)
    contact_person = 'deva.nadesan@infinitom.com'

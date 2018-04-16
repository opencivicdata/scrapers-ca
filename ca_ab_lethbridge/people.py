from utils import CSVScraper

from datetime import date


class LethbridgePersonScraper(CSVScraper):
    csv_url = 'https://docs.google.com/spreadsheets/d/1OnHJq_j-r3R4MMkRQ5ahNkApuDp1NpTYn4UVTTNGY5c/pub?gid=908195318&single=true&output=csv'
    many_posts_per_area = True
    updated_at = date(2017, 11, 8)
    contact_person = 'annelies@avowebworks.ca'

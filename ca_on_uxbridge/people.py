from utils import CSVScraper

from datetime import date


class UxbridgePersonScraper(CSVScraper):
    csv_url = 'https://docs.google.com/spreadsheets/d/1NIW_hM8gm0AlbTvWGBXaBU9DTeom74z5ZhrA10Z94G4/pub?gid=171849574&single=true&output=csv'
    many_posts_per_area = True
    unique_roles = ('Mayor', 'Regional Councillor')
    created_at = date(2016, 11, 23)
    contact_person = 'joe.murray@jmaconsulting.biz'

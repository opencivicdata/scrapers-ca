from datetime import date

from utils import CSVScraper


class UxbridgePersonScraper(CSVScraper):
    csv_url = "https://docs.google.com/spreadsheets/d/1NIW_hM8gm0AlbTvWGBXaBU9DTeom74z5ZhrA10Z94G4/pub?gid=171849574&single=true&output=csv"
    updated_at = date(2018, 11, 13)
    contact_person = "joe.murray@jmaconsulting.biz"

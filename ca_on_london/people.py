from utils import CSVScraper


class LondonPersonScraper(CSVScraper):
    # https://www.london.ca/city-hall/open-data/Pages/Open-Data-Data-Catalogue.aspx
    csv_url = 'http://apps.london.ca/OpenData/CSV/Council.csv'

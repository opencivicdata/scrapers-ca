from utils import CSVScraper


class BramptonPersonScraper(CSVScraper):
    csv_url = 'https://opendata.arcgis.com/datasets/e03b439638434453bb6917732a1e2ddd_0.csv'
    encoding = 'utf-8-sig'

from utils import CSVScraper


class LondonPersonScraper(CSVScraper):
    # "Elected officials' contact information"
    # https://opendata.london.ca/datasets/6345aeda8fa74917a2500e66a3bb432e/about
    csv_url = "https://www.arcgis.com/sharing/rest/content/items/6345aeda8fa74917a2500e66a3bb432e/data"
    encoding = "utf8-sig"

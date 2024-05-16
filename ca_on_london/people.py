from utils import CSVScraper


class LondonPersonScraper(CSVScraper):
    # "Elected officials' contact information"
    # https://opendata.london.ca/datasets/6345aeda8fa74917a2500e66a3bb432e/about
    csv_url = "https://opendata.arcgis.com/datasets/6345aeda8fa74917a2500e66a3bb432e_0.csv"
    encoding = "utf8-sig"

from utils import CSVScraper


class WindsorPersonScraper(CSVScraper):
    # https://open-data-portal-citywindsor.hub.arcgis.com/datasets/8b368e9402cd4cac8e875911a6354e55/about
    csv_url = "https://mappmycity.ca/open_data_files/City%20Windsor%20Elected%20Officials.csv"

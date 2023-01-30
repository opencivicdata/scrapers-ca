from utils import CSVScraper


class WaterlooPersonScraper(CSVScraper):
    # http://opendata-city-of-waterloo.opendata.arcgis.com/datasets/city-of-waterloo-elected-officials
    csv_url = "http://opendata-city-of-waterloo.opendata.arcgis.com/datasets/594698f0bbcd4c20b72977194d2b97b8_0.csv"

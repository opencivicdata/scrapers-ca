from utils import CSVScraper


class KitchenerPersonScraper(CSVScraper):
    # http://open-kitchenergis.opendata.arcgis.com/datasets/aa7c40a2bb5c4c95b3a373ff23844aab
    csv_url = "https://app2.kitchener.ca/appdocs/opendata/staticdatasets/Elected_Officials.csv"

from utils import CSVScraper


class BramptonPersonScraper(CSVScraper):
    # http://geohub.brampton.ca/datasets/term-of-council-elected-officials-2018-to-2022
    csv_url = "https://opendata.arcgis.com/datasets/c6ba9407f9ec4771b575a3c5ee3f89d3_0.csv"
    encoding = "utf-8-sig"
    corrections = {
        "district name": lambda value: value.capitalize(),
    }

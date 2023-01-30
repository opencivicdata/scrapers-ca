import re

from utils import CSVScraper


class WaterlooPersonScraper(CSVScraper):
    # https://rowopendata-rmw.opendata.arcgis.com/datasets/a6f9364a68644b628ae7faa3b931b1b6_0
    csv_url = "https://opendata.arcgis.com/datasets/a6f9364a68644b628ae7faa3b931b1b6_0.csv"
    corrections = {
        "district name": lambda value: re.sub(r"(?:City|Region|Township) of ", "", value),
        "primary role": {
            "Regional Chair": "Chair",
        },
        "twitter": lambda value: re.sub(r"^@", "https://twitter.com/", value),
    }

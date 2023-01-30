from utils import CSVScraper


class BrantfordPersonScraper(CSVScraper):
    # http://data-brantford.opendata.arcgis.com/datasets/city-of-brantford-elected-officials-2014-to-2018
    csv_url = "https://opendata.arcgis.com/datasets/320d27b8b20a467f8283a78835a33003_0.csv"
    encoding = "utf-8-sig"
    many_posts_per_area = True
    corrections = {
        "primary role": {
            "Ward 1 Councillor": "Councillor",
            "Ward 2 Councillor": "Councillor",
            "Ward 3 Councillor": "Councillor",
            "Ward 4 Councillor": "Councillor",
            "Ward 5 Councillor": "Councillor",
        },
    }

    # Not the Represent CSV Schema.
    def header_converter(self, s):
        return {
            "POSITION": "primary role",
            "NAME": "name",
            "WARD": "district id",
            "WARD_NAME": "district name",
            "EMAIL": "email",
            "MOBILE": "cell",
        }.get(s, s)

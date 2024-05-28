from utils import CSVScraper


class HuronPersonScraper(CSVScraper):
    # https://data-huron.opendata.arcgis.com/datasets/051e72a02edc4337af8ca2606ab58644_0
    csv_url = "https://opendata.arcgis.com/datasets/051e72a02edc4337af8ca2606ab58644_0.csv"
    encoding = "utf-8-sig"
    many_posts_per_area = True
    corrections = {
        "primary role": {
            "Councilor": "Councillor",
        },
        "phone": lambda value: value.replace(", ", ";"),
    }

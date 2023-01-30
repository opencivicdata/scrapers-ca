from utils import CSVScraper


class OakvillePersonScraper(CSVScraper):
    # https://portal-exploreoakville.opendata.arcgis.com/datasets/99b4f905aa5b4bf9a3ada765164a98c1_0
    csv_url = "https://opendata.arcgis.com/datasets/99b4f905aa5b4bf9a3ada765164a98c1_0.csv"
    corrections = {
        "primary role": {
            "Town Councillor": "Councillor",
            "Regional and Town Councillor": "Regional Councillor",
        },
    }

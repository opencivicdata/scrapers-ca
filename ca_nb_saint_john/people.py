from utils import CSVScraper


class SaintJohnPersonScraper(CSVScraper):
    # http://catalogue-saintjohn.opendata.arcgis.com/datasets/municipal-elected-officials
    csv_url = "https://opendata.arcgis.com/datasets/256aed00cd13455cac721eb56769c4d4_0.csv"
    many_posts_per_area = True
    corrections = {
        "district name": {
            "City of Saint John": "Saint John",
        },
    }

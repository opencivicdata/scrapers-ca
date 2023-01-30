from utils import CSVScraper


class VictoriaPersonScraper(CSVScraper):
    # http://opendata.victoria.ca/datasets/councillor-contact-information-2018-2022
    csv_url = "https://opendata.arcgis.com/datasets/d524b5f7e64b40a5ae118dde1852fc22_0.csv?outSR=4326"
    many_posts_per_area = True

from utils import CSVScraper


class GrandePrairiePersonScraper(CSVScraper):
    # https://data.cityofgp.com/Community/City-Council-Contact-Information/vcfc-gi78
    csv_url = "https://data.cityofgp.com/api/views/vcfc-gi78/rows.csv?accessType=DOWNLOAD"
    many_posts_per_area = True

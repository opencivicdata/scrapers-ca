from utils import CSVScraper


class GrandePrairiePersonScraper(CSVScraper):
    # https://data.cityofgp.com/Community/Elected-Official-Contact-Information/kxpv-69sa
    csv_url = 'https://data.cityofgp.com/api/views/kxpv-69sa/rows.csv?accessType=DOWNLOAD'
    many_posts_per_area = True

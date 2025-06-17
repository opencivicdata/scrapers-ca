from utils import CSVScraper


class KelownaPersonScraper(CSVScraper):
    # http://opendata.kelowna.ca/datasets/council-contact-information
    csv_url = "https://www.arcgis.com/sharing/rest/content/items/9333b66380424479816685a9fe44f06f/data"
    many_posts_per_area = True

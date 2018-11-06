from utils import CSVScraper


class KelownaPersonScraper(CSVScraper):
    # http://opendata.kelowna.ca/datasets/council-contact-information
    csv_url = 'https://opendata.arcgis.com/datasets/9333b66380424479816685a9fe44f06f_0.csv'
    many_posts_per_area = True

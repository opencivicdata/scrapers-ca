from utils import CSVScraper


class LangleyPersonScraper(CSVScraper):
    csv_url = 'https://opendata.arcgis.com/datasets/daa3ea0f01d24e9b80d837cf2178eb71_0.csv'
    many_posts_per_area = True

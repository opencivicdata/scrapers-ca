from utils import CSVScraper


class MonctonPersonScraper(CSVScraper):
    csv_url = 'https://opendata.arcgis.com/datasets/d81d30cf2b0d4bf7ae7aea5b0acc9d5f_0.csv'
    many_posts_per_area = True
    corrections = {
        'last name': {
            'Th�riault': 'Thériault',
        },
    }

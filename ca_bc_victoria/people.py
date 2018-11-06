from utils import CSVScraper


class VictoriaPersonScraper(CSVScraper):
    # http://opendata.victoria.ca/datasets/councillor-contact-information-2014-2018
    csv_url = 'http://www.victoria.ca/assets/City~Hall/Open~Data/Councillor%20Contact%20Info.csv'
    many_posts_per_area = True

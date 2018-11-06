from utils import CSVScraper


class BurlingtonPersonScraper(CSVScraper):
    # https://navburl-burlington.opendata.arcgis.com/datasets/elected-official-contact
    csv_url = 'https://opendata.arcgis.com/datasets/f2c404c667904f03be38443cbd474cd3_0.csv'

from utils import CSVScraper


class PeelPersonScraper(CSVScraper):
    # http://opendata.peelregion.ca/data-categories/regional-geography/ward-boundaries-(2014-2018).aspx
    csv_url = 'http://opendata.peelregion.ca/media/33531/wards1418_csv.csv'

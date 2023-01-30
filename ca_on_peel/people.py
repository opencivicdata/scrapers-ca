from utils import CSVScraper


class PeelPersonScraper(CSVScraper):
    # http://opendata.peelregion.ca/data-categories/regional-geography/ward-boundaries-(2018-2022).aspx
    csv_url = "http://opendata.peelregion.ca/media/43505/wards1822_csv.csv"

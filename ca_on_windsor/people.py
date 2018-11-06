from utils import CSVScraper


class WindsorPersonScraper(CSVScraper):
    # https://opendata.citywindsor.ca/opendata/details/196
    csv_url = 'http://www.citywindsor.ca/opendata/Lists/OpenData/Attachments/33/City%20Windsor%20Elected%20Officials.csv'

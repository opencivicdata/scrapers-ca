from utils import CSVScraper


class StrathconaCountyPersonScraper(CSVScraper):
    # https://data.strathcona.ca/County-Government/County-Council-2013-2017/suw8-zxcy
    csv_url = 'https://data.strathcona.ca/api/views/suw8-zxcy/rows.csv?accessType=DOWNLOAD'

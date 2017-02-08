from __future__ import unicode_literals
from utils import CSVScraper


class SaskatoonPersonScraper(CSVScraper):
    csv_url = 'https://saskatoonopendataconfig.blob.core.windows.net/converteddata/MayorAndCityCouncilContactInformation.csv'

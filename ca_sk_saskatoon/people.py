from utils import CSVScraper


class SaskatoonPersonScraper(CSVScraper):
    csv_url = 'https://saskatoonopendataconfig.blob.core.windows.net/converteddata/MayorAndCityCouncilContactInformation.csv'

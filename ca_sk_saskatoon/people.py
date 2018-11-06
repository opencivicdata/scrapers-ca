from utils import CSVScraper


class SaskatoonPersonScraper(CSVScraper):
    # http://opendata-saskatoon.cloudapp.net/DataBrowser/SaskatoonOpenDataCatalogueBeta/MayorAndCityCouncilContactInformation
    csv_url = 'https://saskatoonopendataconfig.blob.core.windows.net/converteddata/MayorAndCityCouncilContactInformation.csv'

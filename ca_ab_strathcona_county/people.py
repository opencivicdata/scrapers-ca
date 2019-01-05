from utils import CSVScraper


class StrathconaCountyPersonScraper(CSVScraper):
    # https://data.strathcona.ca/County-Government/County-Council-2017-2021/3znf-p2na
    csv_url = 'https://data.strathcona.ca/api/views/3znf-p2na/rows.csv?accessType=DOWNLOAD'
    corrections = {
        'district name': {
            'Strathcona': 'Strathcona County',
        }
    }

    def header_converter(self, s):
        s = super(StrathconaCountyPersonScraper, self).header_converter(s)
        if s == 'district id':
            return 'district name'
        return s

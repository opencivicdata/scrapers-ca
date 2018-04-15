from utils import CSVScraper


class BramptonPersonScraper(CSVScraper):
    csv_url = 'https://opendata.arcgis.com/datasets/e03b439638434453bb6917732a1e2ddd_0.csv'

    def header_converter(self, s):
        return super(BramptonPersonScraper, self).header_converter(s.replace('\ufeff', ''))

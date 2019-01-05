from utils import CSVScraper


class OakvillePersonScraper(CSVScraper):
    # https://portal-exploreoakville.opendata.arcgis.com/datasets/toak::oakville-town-council
    csv_url = 'http://opendata.oakville.ca/Oakville_Town_Council/Oakville_Town_Council.csv'
    encoding = 'windows-1252'
    corrections = {
        'primary role': {
            'Town Councillor': 'Councillor',
            'Regional and Town Councillor': 'Regional Councillor',
        },
    }

    def header_converter(self, s):
        return super(OakvillePersonScraper, self).header_converter(s).replace('phone (cell)', 'cell')

from utils import CSVScraper


class WaterlooPersonScraper(CSVScraper):
    csv_url = 'http://www.regionofwaterloo.ca/opendatadownloads/RegionalMunicipalityOfWaterlooCouncil_2014_2018.xls'
    corrections = {
        'district name': {
            'City of Cambridge': 'Cambridge',
            'City of Kitchener': 'Kitchener',
            'City of Waterloo': 'Waterloo',
            'Region of Waterloo': 'Waterloo',
            'Township of North Dumfries': 'North Dumfries',
            'Township of Wellesley': 'Wellesley',
            'Township of Wilmot': 'Wilmot',
            'Township of Woolwich': 'Woolwich',
        },
        'primary role': {
            'Regional Chair': 'Chair',
        },
    }

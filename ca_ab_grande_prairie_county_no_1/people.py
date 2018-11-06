from utils import CSVScraper


class GrandePrairieCountyNo1PersonScraper(CSVScraper):
    # https://data1-cogp.opendata.arcgis.com/datasets?t=election
    csv_url = 'http://data.countygp.ab.ca/data/ElectedOfficials/elected-officials.csv'

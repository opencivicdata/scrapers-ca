from utils import CSVScraper


class KingstonPersonScraper(CSVScraper):
    # https://opendatakingston.cityofkingston.ca/datasets/887f5b625f6c41b2bde402603ba14d55_0/explore
    csv_url = "https://services1.arcgis.com/5GRYvurYYUwAecLQ/arcgis/rest/services/Council_Contact_List/FeatureServer/replicafilescache/Council_Contact_List_1489158215873276683.csv"

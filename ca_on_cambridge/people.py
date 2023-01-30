from utils import CSVScraper


class CambridgePersonScraper(CSVScraper):
    # http://geohub.cambridge.ca/datasets/elected-officials
    csv_url = "https://maps.cambridge.ca/Images/OpenData/SharedDocuments/ElectedOfficials.csv"

from __future__ import unicode_literals
from utils import CSVScraper


class CambridgePersonScraper(CSVScraper):
    csv_url = 'https://maps.cambridge.ca/Images/OpenData/SharedDocuments/ElectedOfficials.csv'

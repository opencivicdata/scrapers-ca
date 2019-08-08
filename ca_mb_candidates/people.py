from utils import CSVScraper
from datetime import date


class ManitobaCandidatesPersonScraper(CSVScraper):
    csv_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTVIRhSoEfhyLiRo0ggcSDilLCwLJlLPgQ-FI_4oXJ3EW3C-PKcl8pQynjKD2v1aR-iRzKc2P_hPsjK/pub?output=csv'
    updated_at = date(2019, 7, 8)
    contact_person = 'andrew@newmode.net'
    encoding = 'utf-8'
    corrections = {
        'district name': {
        }
    }

    def is_valid_row(self, row):
        return any(row.values()) and row['last name'] and row['first name']

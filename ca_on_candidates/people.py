from utils import CSVScraper

from datetime import date


class BritishColumbiaCandidatesPersonScraper(CSVScraper):
    csv_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQhrWSeOEC9DaNN2iDKcPC9IH701Al0pELevzSO62maI9WXt1TGvFH2fzUkXjUfujc3ontePcroFbT2/pub?output=csv'
    created_at = date(2018, 1, 31)
    contact_person = 'andrew@newmode.net'
    #corrections = {}

    def is_valid_row(self, row):
        return any(row.values()) and row['last name'] and row['first name']

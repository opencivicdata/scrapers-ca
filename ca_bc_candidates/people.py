from __future__ import unicode_literals
from utils import CSVScraper

from datetime import date


class BritishColumbiaCandidatesPersonScraper(CSVScraper):
    csv_url = 'https://docs.google.com/spreadsheets/d/1eleD97boUkc8d8O1pR1U_nfpeKd_707SSiCPzSIvJ-c/pub?gid=0&single=true&output=csv'
    created_at = date(2017, 2, 6)
    contact_person = 'andrew@newmode.net'

    def is_valid_row(self, row):
        return any(row.values()) and row['last name'] and row['first name']

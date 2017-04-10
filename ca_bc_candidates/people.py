from utils import CSVScraper

from datetime import date


class BritishColumbiaCandidatesPersonScraper(CSVScraper):
    csv_url = 'https://docs.google.com/spreadsheets/d/1eleD97boUkc8d8O1pR1U_nfpeKd_707SSiCPzSIvJ-c/pub?gid=0&single=true&output=csv'
    created_at = date(2017, 2, 6)
    contact_person = 'andrew@newmode.net'
    corrections = {
        'party_name': {
            'British Columbia Conservatives': "British Columbia Conservative Party",
            'Communist Party of British Columbia': "Communist Party of BC",
            'Communist': "Communist Party of BC",
            'Green Party of British Columbia': "Green Party Political Association of British Columbia",
            'Libertarian': "British Columbia Libertarian Party",
            'New Democratic Party of British Columbia': "BC NDP",
        }
    }

    def is_valid_row(self, row):
        return any(row.values()) and row['last name'] and row['first name']

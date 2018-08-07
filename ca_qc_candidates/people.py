from utils import CSVScraper

from datetime import date


class QuebecCandidatesPersonScraper(CSVScraper):
    csv_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSReKYYQs878kjmuMnMOtYusEP1DDmVBlWaMfJqFEtcpb87NtklZqmYfTn_xD8hu-OLjIOignv6T5x8/pub?gid=0&single=true&output=csv'
    updated_at = date(2018, 8, 6)
    contact_person = 'xavier@mutualit.org'
    encoding = 'utf-8'
    locale = 'fr'
    corrections = {
        'twitter': {
            'ND': '',
        },
        'website': {
            'ND': '',
        },
    }

    def is_valid_row(self, row):
        return any(row.values()) and row['last name'] and row['party name']

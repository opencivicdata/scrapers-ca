from utils import CSVScraper

from datetime import date


class CalgaryCandidatesPersonScraper(CSVScraper):
    csv_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQhrWSeOEC9DaNN2iDKcPC9IH701Al0pELevzSO62maI9WXt1TGvFH2fzUkXjUfujc3ontePcroFbT2/pub?gid=757164835&single=true&output=csv'
    created_at = date(2017, 8, 26)
    contact_person = 'shamus@newmode.net'

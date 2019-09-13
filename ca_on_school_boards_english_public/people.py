from utils import CSVScraper
from datetime import date


class OntarioEnglishPublicSchoolBoardsPersonScraper(CSVScraper):
    csv_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTbnQN0j_2Ky56MeRQsNTYXnt9Q6f_vFgH_KyAZ3O96QhjLqMK_Fzrjz2lI8ympE1FU0lkKgbGEvjW0/pub?gid=785048945&single=true&output=csv'
    # CSV source: https://docs.google.com/spreadsheets/d/1smXFR3nB9lovc6bWWcLvr621wb6E5b2TZKqUtxRTUtE/edit#gid=785048945
    updated_at = date(2019, 9, 13)
    contact_person = 'andrew@newmode.net'
    encoding = 'utf-8'
    corrections = {
        'district name': {
        }
    }

    def is_valid_row(self, row):
        return any(row.values()) and row['last name'] and row['first name']

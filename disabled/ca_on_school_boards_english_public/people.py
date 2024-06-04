from datetime import date

from utils import CSVScraper


class OntarioEnglishPublicSchoolBoardsPersonScraper(CSVScraper):
    # CSV source: https://docs.google.com/spreadsheets/d/1smXFR3nB9lovc6bWWcLvr621wb6E5b2TZKqUtxRTUtE/edit#gid=785048945
    csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTbnQN0j_2Ky56MeRQsNTYXnt9Q6f_vFgH_KyAZ3O96QhjLqMK_Fzrjz2lI8ympE1FU0lkKgbGEvjW0/pub?gid=785048945&single=true&output=csv"
    updated_at = date(2019, 9, 13)
    contact_person = "andrew@newmode.net"
    many_posts_per_area = True
    unique_roles = ["Chair"]
    encoding = "utf-8"
    corrections = {"district name": {}}
    organization_classification = "committee"

    def is_valid_row(self, row):
        return any(row.values()) and row["last name"] and row["first name"]

from datetime import date

from utils import CSVScraper


class ManitobaCandidatesPersonScraper(CSVScraper):
    # Source: https://docs.google.com/spreadsheets/d/1Qacn9um-HC1qjN7_008wPl3AxgvbQuBPsT-Umh_FiPQ/edit?usp=sharing
    csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRWR5loiU8ZHl1308iT95bJmQw9XDkCabW_3Pxn1XK9z6dPLqLzgsjrPWAgOlPbNXjZtgwsesxxP3bj/pub?gid=0&single=true&output=csv"
    updated_at = date(2019, 7, 8)
    contact_person = "andrew@newmode.net"
    encoding = "utf-8"

    def is_valid_row(self, row):
        return any(row.values()) and row["last name"] and row["first name"]

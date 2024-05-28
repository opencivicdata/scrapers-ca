from datetime import date

from utils import CSVScraper


class AlbertaCandidatesPersonScraper(CSVScraper):
    csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR4i0tdtPJxFSXAccxZ1rjl8aIT-HApNcFs7In-thJJeLi4rKkXZMxIXkF1W0h_tK58QBgb3TZiEjQG/pub?output=csv"
    updated_at = date(2019, 3, 7)
    contact_person = "mark@newmode.net"
    encoding = "utf-8"
    corrections = {"district name": {}}

    def is_valid_row(self, row):
        return any(row.values()) and row["last name"] and row["first name"]

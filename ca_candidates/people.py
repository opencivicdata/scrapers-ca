from datetime import date

from utils import CSVScraper


class CanadaCandidatesPersonScraper(CSVScraper):
    csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQg-GxpZeCdOMumAu5AbmDC6Ff2fXpcnSkIGaKTbow_PPwtznC4riqKxBuJZlX4c7XB4n7opnPzFdGI/pub?output=csv"
    updated_at = date(2019, 4, 17)
    contact_person = "andrew@newmode.net"
    encoding = "utf-8"
    corrections = {"district name": {}}

    def is_valid_row(self, row):
        return any(row.values()) and row["last name"] and row["first name"]

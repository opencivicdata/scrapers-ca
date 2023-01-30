import re

from utils import CSVScraper


class NiagaraPersonScraper(CSVScraper):
    # https://niagaraopendata.ca/dataset/council-elected-officials
    csv_url = "https://niagaraopendata.ca/dataset/ee767222-c7fc-4541-8cad-a27276a3522b/resource/f409257f-5a6d-4719-a326-2719dd5c43ff/download/2018---2022-council-elected-officials.csv"
    many_posts_per_area = True
    corrections = {
        "district name": lambda value: re.sub(r"Niagara Region", "Niagara", re.sub(r"Niagara Region - ", "", value))
    }

    def header_converter(self, s):
        s = super().header_converter(s)
        if s == "district id":
            return "district name"
        return s

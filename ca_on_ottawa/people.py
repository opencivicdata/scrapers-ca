# coding: utf-8
from utils import CSVScraper


class OttawaPersonScraper(CSVScraper):
    # http://data.ottawa.ca/dataset/elected-officials
    csv_url = "http://data.ottawa.ca/dataset/fd26ae83-fe1a-40d8-8951-72df40021c82/resource/3cd1b14d-cb45-4c4d-b22a-a607946e2ec2/download/elected-officials-2018-2022.csv"
    encoding = "utf-8-sig"
    corrections = {
        "district name": {
            "Orl\u0082ans": "Orléans",
        },
    }

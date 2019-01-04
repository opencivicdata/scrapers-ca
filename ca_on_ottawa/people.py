# coding: utf-8
from utils import CSVScraper


class OttawaPersonScraper(CSVScraper):
    # http://data.ottawa.ca/dataset/elected-officials
    csv_url = 'http://data.ottawa.ca/dataset/fd26ae83-fe1a-40d8-8951-72df40021c82/resource/2006818a-e5db-493f-bd06-4c2cc85cf26e/download/elected-officials-2018-2022.csv'
    encoding = 'utf-8-sig'
    corrections = {
        'district name': {
            "Orl\u0082ans": 'Orléans',
        },
    }

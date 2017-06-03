# coding: utf-8
from utils import CSVScraper


class OttawaPersonScraper(CSVScraper):
    csv_url = 'http://data.ottawa.ca/en/dataset/fd26ae83-fe1a-40d8-8951-72df40021c82/resource/33a437d3-a06d-4c56-a7fe-4fd622364ce6/download/elected-officials-282014-201829-v.2.csv'
    corrections = {
        'district name': {
            "Orl\u0082ans": 'Orléans',
        },
    }
from utils import CSVScraper

import re


class NiagaraPersonScraper(CSVScraper):
    # https://niagaraopendata.ca/dataset/council-elected-officials
    csv_url = 'https://niagaraopendata.ca/dataset/ee767222-c7fc-4541-8cad-a27276a3522b/resource/af5621ad-c2e4-4569-803f-4aadca4173be/download/councilelectedofficials.csv'
    many_posts_per_area = True
    corrections = {
        'district name': lambda value: re.sub(r'Niagara Region', 'Niagara', re.sub(r'Niagara Region - ', '', value))
    }

    def header_converter(self, s):
        s = super(NiagaraPersonScraper, self).header_converter(s)
        if s == 'district id':
            return 'district name'
        return s

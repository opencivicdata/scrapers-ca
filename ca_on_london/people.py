from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

import re

COUNCIL_PAGE = 'http://www.london.ca/city-hall/city-council/Pages/default.aspx'
COUNCIL_CSV_URL = 'http://apps.london.ca/OpenData/CSV/Council.csv'


class LondonPersonScraper(CanadianScraper):

    def scrape(self):
        csv = self.csv_reader(COUNCIL_CSV_URL, header=True)
        for row in csv:
            district = row['District name']
            role = row['Elected office']
            name = '%s %s' % (row['First name'], row['Last name'])

            p = Person(primary_org='legislature', name=name, district=district, role=role)
            p.add_source(COUNCIL_CSV_URL)
            if row['URL']:
                p.add_source(row['URL'])
            if row['Gender']:
                p.gender = row['Gender']
            if row['Photo URL']:
                p.image = row['Photo URL']
            p.add_contact('email', row['Email'])
            p.add_contact('address', row['Address'], row['Office type'])
            p.add_contact('voice', row['Phone'], row['Office type'])
            if row['Fax']:
                p.add_contact('fax', row['Fax'], row['Office type'])
            if row['Facebook']:
                p.add_link(re.sub(r'[#?].+', '', row['Facebook']))
            if row['Twitter']:
                p.add_link(row['Twitter'])
            yield p

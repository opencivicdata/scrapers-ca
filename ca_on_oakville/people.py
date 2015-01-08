from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.oakville.ca/townhall/council.html'
COUNCIL_CSV_URL = 'http://opendata.oakville.ca/Oakville_Town_Council/Oakville_Town_Council.csv'


class OakvillePersonScraper(CanadianScraper):

    def scrape(self):
        csv = self.csv_reader(COUNCIL_CSV_URL, header=True, encoding='windows-1252')
        for row in csv:
            district = row['District name']
            role = row['Primary role']
            name = '%s %s' % (row['First name'], row['Last name'])

            if role == 'Town Councillor':
                role = 'Councillor'

            address = row['Address line 1']
            if row['Address line 2']:
                address += '\n%s' % row['Address line 2']
            address += '\n%s ON  %s' % (row['Locality'], row['Postal code'])

            p = Person(primary_org='legislature', name=name, district=district, role=role)
            p.add_source(COUNCIL_CSV_URL)
            p.add_source(row['Source URL'])
            if row['Gender']:
                p.gender = row['Gender']
            p.image = row['Photo URL']
            p.add_contact('email', row['Email'])
            p.add_contact('address', address, 'legislature')
            p.add_contact('voice', row['Phone'], 'legislature')
            if row['Fax']:
                p.add_contact('fax', row['Fax'], 'legislature')
            if row['Phone (cell)']:
                p.add_contact('cell', row['Phone (cell)'], 'legislature')
            yield p

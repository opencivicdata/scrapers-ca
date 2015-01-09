from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

from collections import defaultdict

COUNCIL_PAGE = 'http://www.welland.ca/Council/index.asp'
COUNCIL_CSV_URL = 'http://www.welland.ca/open/Datasheets/Welland_mayor_and_council_members.csv'


class WellandPersonScraper(CanadianScraper):

    def scrape(self):
        seat_numbers = defaultdict(int)

        csv = self.csv_reader(COUNCIL_CSV_URL, header=True, encoding='windows-1252')
        for row in csv:
            district = row['District name']
            role = row['Primary role']
            name = '%s %s' % (row['First name'], row['Last name'])

            if 'Ward' in district:
                seat_numbers[district] += 1
                district = '%s (seat %d)' % (district, seat_numbers[district])

            address = row['Address line 1']
            if row['Address line 2']:
                address += '\n%s' % row['Address line 2']
            address += '\n%s ON  %s' % (row['Locality'], row['Postal code'])

            p = Person(primary_org='legislature', name=name, district=district, role=role)
            p.add_source(COUNCIL_CSV_URL)
            if row['Source URL']:
                p.add_source(row['Source URL'])
            if row['Gender']:
                p.gender = row['Gender']
            if row['Photo URL']:
                p.image = row['Photo URL']
            p.add_contact('email', row['Email'])
            p.add_contact('address', address, 'legislature')
            p.add_contact('voice', row['Phone'], 'legislature')
            if row['Fax']:
                p.add_contact('fax', row['Fax'], 'legislature')
            yield p

from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://guelph.ca/city-hall/mayor-and-council/city-council/'
COUNCIL_CSV_URL = 'http://open.guelph.ca/wp-content/uploads/2014/12/GuelphCityCouncil2014-2018ElectedOfficalsContactInformation.csv'


class GuelphPersonScraper(CanadianScraper):

    def scrape(self):
        csv = self.csv_reader(COUNCIL_CSV_URL, header=True)
        for row in csv:
            district = row['District name']
            role = row['Primary role']
            name = '%s %s' % (row['First name'], row['Last name'])

            address = row['Address line 1']
            if row['Address line 2']:
                address += '\n%s' % row['Address line 2']
            address += '\n%s ON  %s' % (row['Locality'], row['Postal code'])

            p = Person(primary_org='legislature', name=name, district=district, role=role)
            p.add_source(COUNCIL_CSV_URL)
            p.add_source(row['Source URL'])
            p.gender = row['Gender']
            p.image = row['Photo URL']
            p.add_contact('email', row['Email'])
            p.add_contact('address', address, 'legislature')
            p.add_contact('voice', row['Phone'], 'legislature')
            p.add_contact('fax', row['Fax'], 'legislature')
            if row['Phone (mobile)']:
                p.add_contact('cell', row['Phone (mobile)'], 'legislature')
            yield p

from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://vancouver.ca/your-government/vancouver-city-council.aspx'


class VancouverPersonScraper(CanadianScraper):
    csv_url = 'ftp://webftp.vancouver.ca/OpenData/csv/CouncilContactInformation.csv'

    def scrape(self):
        councillor_seat_number = 1

        for row in self.csv_reader(self.csv_url, header=True):
            if row['Elected Office'] == 'Mayor':
                district = 'Vancouver'
            else:
                district = 'Vancouver (seat %d)' % councillor_seat_number
                councillor_seat_number += 1

            p = Person(
                primary_org='legislature',
                name='%(First Name)s %(Last Name)s' % row,
                district=district,
                role=row['Elected Office'],
                gender=row['Gender'],
                image=row['Photo URL'],
            )
            p.add_contact('email', row['Email'])
            p.add_contact('voice', row['Phone'], 'legislature')
            p.add_contact('fax', row['Fax'], 'legislature')
            p.add_contact('address', '%(Address line 1)s\n%(Locality)s %(Province)s  %(Postal Code)s' % row, 'legislature')
            p.add_source(self.csv_url)
            p.add_source(row['URL'])
            yield p

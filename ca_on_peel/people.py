# coding: utf-8
from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://opendata.peelregion.ca/media/25713/ward20102014_csv_12.2013.csv'
CHAIR_URL = 'https://www.peelregion.ca/council/councill/kolb.htm'


class PeelPersonScraper(CanadianScraper):

    def scrape(self):
        yield self.chair_info(CHAIR_URL)
        for row in self.csv_reader(COUNCIL_PAGE, header=True, headers={'Cookie': 'incap_ses_168_68279=7jCHCh608QQSFVti3dtUAviu/1IAAAAAIRf6OsZL0NttnlzANkVb6w=='}):

            p = Person(
                primary_org='legislature',
                name='%(FirstName0)s %(LastName0)s' % row,
                district='%(MUNIC)s Ward %(WARDNUM)s' % row,
                role='Councillor',
            )
            p.add_contact('email', row['email0'])
            p.add_contact('voice', row['Phone0'], 'legislature')
            p._related[0].extras['boundary_url'] = '/boundaries/%s-wards/ward-%s/' % (row['MUNIC'].lower(), row['WARDNUM'])
            p.add_source(COUNCIL_PAGE)
            yield p

            if row['FirstName1'].strip():
                p = Person(
                    primary_org='legislature',
                    name='%s %s' % (row['FirstName1'], row['LastName1']),
                    district='%(MUNIC)s Ward %(WARDNUM)s' % row,
                    role='Councillor',
                )
                p.add_contact('email', row['email1'])
                p.add_contact('voice', row['Phone1'], 'legislature')
                p._related[0].extras['boundary_url'] = '/boundaries/%s-wards/ward-%s/' % (row['MUNIC'].lower(), row['WARDNUM'])
                p.add_source(COUNCIL_PAGE)
                yield p

    def chair_info(self, url):
        page = self.lxmlize(url)
        name = page.xpath('string(//title)').split('-')[1]
        photo_url = page.xpath('string(//div[@class="co-menu"]/img/@src)')
        # sadly, email is script-based
        address = page.xpath('string(//div[@id="co-content"]/p[1])')
        phone = page.xpath('string(//div[@id="co-content"]/p[2]/text())').split(':')[1]

        p = Person(primary_org='legislature', name=name, district='Peel', role='Regional Chair',
                   image=photo_url)
        p.add_source(url)
        p.add_contact('address', address, 'legislature')
        p.add_contact('voice', phone, 'legislature')
        return p

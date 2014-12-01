from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.cityofgp.com/index.aspx?page=718'


class GrandePrairiePersonScraper(CanadianScraper):

    def scrape(self):
        councillor_seat_number = 1

        page = self.lxmlize(COUNCIL_PAGE)
        for row in page.xpath(r'//table[@class="listtable"]//tr')[1:]:
            celltext = row.xpath('./td//text()')
            last, first = celltext[0].split(', ')
            name = ' '.join((first, last))
            role = celltext[1]

            if role == 'Mayor':
                district = 'Grande Prairie'
            else:
                district = 'Grande Prairie (seat %d)' % councillor_seat_number
                councillor_seat_number += 1

            p = Person(primary_org='legislature', name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_contact('voice', celltext[3], 'legislature')
            p.add_contact('email', row.xpath('string(./td[last()]//a/@href)').split(':')[1])
            yield p

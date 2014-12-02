from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.abbotsford.ca/city_hall/mayor_and_council/city_council.htm'

MAYOR_URL = 'http://www.abbotsford.ca/mayorcouncil/city_council/mayor_banman.htm'


class AbbotsfordPersonScraper(CanadianScraper):

    def scrape(self):
        councillor_seat_number = 1

        page = self.lxmlize(COUNCIL_PAGE)
        for link in page.xpath('//div[@id="main-content"]//li/a'):
            text = link.text_content()
            if text.startswith('Councill'):
                role = 'Councillor'
                district = 'Abbotsford (seat %d)' % councillor_seat_number
                councillor_seat_number += 1
            else:
                role = 'Mayor'
                district = 'Abbotsford'
            name = text.split(' ', 1)[1]

            p = Person(primary_org='legislature', name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            yield p

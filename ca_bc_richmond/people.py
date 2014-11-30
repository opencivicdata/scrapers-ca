from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.richmond.ca/cityhall/council.htm'
CONTACT_URL = 'http://www.richmond.ca/contact/departments/council.htm'


class RichmondPersonScraper(CanadianScraper):

    def scrape(self):
        councillor_seat_number = 1

        contact_page = self.lxmlize(CONTACT_URL)
        email = contact_page.xpath('string(//a[starts-with(@href, "mailto:")])')
        page = self.lxmlize(COUNCIL_PAGE)
        for url in page.xpath('//a/@href[contains(., "members/")]'):
            page = self.lxmlize(url)
            role, name = page.xpath('string(//h1)').split(' ', 1)
            # image element is inserted by a script somewhere
            # photo_url = page.xpath('string(//span[@class="imageShadow"]/img/@src)')

            if role == 'Mayor':
                district = 'Richmond'
            else:
                district = 'Richmond (seat %d)' % councillor_seat_number
                councillor_seat_number += 1

            p = Person(primary_org='legislature', name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(CONTACT_URL)
            p.add_source(url)
            p.add_contact('email', email)
            yield p

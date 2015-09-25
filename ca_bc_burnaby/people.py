from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.burnaby.ca/Our-City-Hall/Mayor---Council/Council-Profiles.html'


class BurnabyPersonScraper(CanadianScraper):

    def scrape(self):
        councillor_seat_number = 1

        page = self.lxmlize(COUNCIL_PAGE)

        for person_url in page.xpath('//h4/a/@href'):
            page = self.lxmlize(person_url)

            role, name = page.xpath('//title//text()')[0].split(' ', 1)
            photo_url = page.xpath('//div[@id="content"]//img[@style]/@src')[0]

            contact_node = page.xpath('//div[@id="column-right"]//div[contains(., "Contact")]')
            if contact_node:
                email = self.get_email(contact_node[0])
                phone = self.get_phone(contact_node[0], area_codes=[604, 778])

            if role == 'Mayor':
                district = 'Burnaby'
            else:
                district = 'Burnaby (seat {})'.format(councillor_seat_number)
                councillor_seat_number += 1

            p = Person(primary_org='legislature', name=name, district=district, role=role, image=photo_url)
            p.add_source(COUNCIL_PAGE)
            p.add_source(person_url)
            p.add_contact('email', email)
            if phone:
                p.add_contact('voice', phone, 'legislature')
            yield p

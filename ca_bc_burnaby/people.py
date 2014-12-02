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
            email = self.get_email(page)
            phone = page.xpath('string(//li//text()[contains(., "Phone:")]|//li//text()[contains(., "Cell:")])')  # can be empty

            if role == 'Mayor':
                district = 'Burnaby'
            else:
                district = 'Burnaby (seat %d)' % councillor_seat_number
                councillor_seat_number += 1

            p = Person(primary_org='legislature', name=name, district=district, role=role, image=photo_url)
            p.add_source(COUNCIL_PAGE)
            p.add_source(person_url)
            p.add_contact('email', email)
            if phone:
                p.add_contact('voice', phone, 'legislature')
            yield p

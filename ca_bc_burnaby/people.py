from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.burnaby.ca/Our-City-Hall/Mayor---Council/Council-Profiles.html'


class BurnabyPersonScraper(CanadianScraper):

    def scrape(self):
        councillor_seat_number = 1

        page = self.lxmlize(COUNCIL_PAGE)

        for person_url in page.xpath('//h4/a/@href'):
            page = self.lxmlize(person_url)

            role, name = page.xpath('string(//title)').split(' ', 1)
            photo_url = page.xpath('//div[@id="content"]//img[@style]/@src')[0]
            email = page.xpath('string(//a[contains(@href, "mailto:")])')
            phone = page.xpath('string(//li[contains(text(), "Phone:")])')

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

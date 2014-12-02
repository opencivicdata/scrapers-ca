from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.stjohns.ca/city-hall/about-city-hall/council'


class StJohnsPersonScraper(CanadianScraper):

    def scrape(self):
        councillor_seat_number = 1

        page = self.lxmlize(COUNCIL_PAGE)
        nodes = page.xpath('//div[@class="view-content"]/div')
        for node in nodes:
            fields = node.xpath('./div')
            role = fields[0].xpath('./div//text()')[0]
            name = fields[2].xpath('.//a//text()')[0].title().split(role)[-1]
            if 'Ward' in role:
                district = role
                role = 'Councillor'
            else:
                if 'At Large' in role:
                    role = 'Councillor at Large'
                    district = "St. John's (seat %d)" % councillor_seat_number
                    councillor_seat_number += 1
                else:
                    district = "St. John's"
            phone = fields[3].xpath('./div//text()')[0]
            email = self.get_email(fields[5])
            photo_url = node.xpath('.//img/@src')[0]

            p = Person(primary_org='legislature', name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_contact('voice', phone, 'legislature')
            p.add_contact('email', email)
            p.image = photo_url
            yield p

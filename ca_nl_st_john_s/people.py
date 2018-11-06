from utils import CanadianScraper, CanadianPerson as Person

import re

COUNCIL_PAGE = 'http://www.stjohns.ca/city-hall/about-city-hall/council'


class StJohnsPersonScraper(CanadianScraper):
    def scrape(self):
        councillor_seat_number = 1

        page = self.lxmlize(COUNCIL_PAGE)
        councillors = page.xpath('//div[@class="view-content"]/div')
        assert len(councillors), 'No councillors found'
        for node in councillors:
            fields = node.xpath('./div')
            district_or_role = fields[0].xpath('./div//text()')[0]
            if 'At Large' in district_or_role:
                district_or_role = re.sub(r' \d', '', district_or_role)

            name = fields[2].xpath('.//a//text()')[0].title().split(district_or_role)[-1].strip()
            if name == 'Vacant':
                continue

            if 'Ward' in district_or_role:
                district = district_or_role
                role = 'Councillor'
            else:
                if 'At Large' in district_or_role:
                    district = "St. John's (seat {})".format(councillor_seat_number)
                    role = 'Councillor at Large'
                    councillor_seat_number += 1
                else:
                    district = "St. John's"
                    role = district_or_role

            phone = fields[3].xpath('./div//text()')[0]
            email = self.get_email(fields[4])
            photo_url = node.xpath('.//img/@src')[0]

            p = Person(primary_org='legislature', name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_contact('voice', phone, 'legislature')
            p.add_contact('email', email)
            p.image = photo_url
            yield p

from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

import re

COUNCIL_PAGE = 'http://www.town.lasalle.on.ca/en/town-hall/LaSalle-Council.asp'


class LaSallePersonScraper(CanadianScraper):

    def scrape(self):
        councillor_seat_number = 1

        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//table[@id="Table1table"]//td/p')
        for councillor in councillors:
            if not councillor.text_content().strip():
                continue
            name = councillor.xpath('./font/b/text()')
            if not name:
                name = councillor.xpath('./font/text()')
            if 'email' in name[0]:
                name = councillor.xpath('./b/font/text()')
            name = name[0]
            role = 'Councillor'
            if 'Mayor' in name:
                name = name.replace('Mayor', '')
                role = 'Mayor'
                district = "LaSalle"
            else:
                district = 'LaSalle (seat {})'.format(councillor_seat_number)
                councillor_seat_number += 1

            p = Person(primary_org='legislature', name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            photo_url = councillor.xpath('./parent::td//img/@src')[0]
            p.image = photo_url

            email = self.get_email(councillor)
            p.add_contact('email', email)

            phone = re.findall(r'(?<=phone:)(.*)(?=home)', councillor.text_content(), flags=re.DOTALL)
            if phone:
                p.add_contact('voice', phone[0].strip(), 'legislature')

            home_phone = re.findall(r'(?<=home phone:)(.*)', councillor.text_content(), flags=re.DOTALL)[0]
            p.add_contact('voice', home_phone.strip(), 'residence')
            yield p

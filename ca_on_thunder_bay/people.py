from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

import re

COUNCIL_PAGE = 'http://www.thunderbay.ca/City_Government/Your_Council.htm'


class ThunderBayPersonScraper(CanadianScraper):

    def scrape(self):
        councillor_seat_number = 1
        page = self.lxmlize(COUNCIL_PAGE)

        mayor = page.xpath('//div/a[contains(@title, "Profile")][1]/@href')
        councillors = mayor + page.xpath('//td//a[contains(@title, "Profile")][1]/@href')
        for councillor in councillors:
            page = self.lxmlize(councillor)
            info = page.xpath('//table/tbody/tr/td[2]')[0]

            for br in info.xpath('*//br'):
                br.tail = '\n' + br.tail if br.tail else '\n'
            lines = [line.strip() for line in info.text_content().split('\n') if line.strip()]
            name = lines[0].replace('Councillor ', '').replace('Mayor ', '')

            if lines[1].endswith(' Ward'):
                district = lines[1].replace(' Ward', '')
                role = 'Councillor'
            elif lines[1] == 'At Large':
                role = 'Councillor at Large'
                district = 'Thunder Bay (seat %d)' % councillor_seat_number
                councillor_seat_number += 1
            else:
                district = 'Thunder Bay'
                role = 'Mayor'
            name = name.replace('Councillor', '').replace('At Large', '').replace('Mayor', '').strip()

            p = Person(primary_org='legislature', name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(councillor)

            p.image = page.xpath('//td[@valign="top"]/img/@src')[0]

            address = ', '.join(info.xpath('./p/text()')[0:2]).strip()
            address = re.sub(r'\s{2,}', ' ', address)

            p.add_contact('address', address, 'legislature')

            contacts = info.xpath('./p[2]/text()')
            for contact in contacts:
                contact_type, contact = contact.replace('Cel:', 'Cell:').split(':')
                contact = contact.replace('(1st)', '').replace('(2nd)', '').strip()
                if 'Fax' in contact_type:
                    p.add_contact('fax', contact, 'legislature')
                elif 'Email' in contact_type:
                    break
                else:
                    p.add_contact('voice', contact, contact_type)

            email = self.get_email(info)
            p.add_contact('email', email)

            yield p

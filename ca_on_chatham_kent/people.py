from __future__ import unicode_literals

import re

from utils import CanadianScraper, CanadianPerson as Person, CONTACT_DETAIL_TYPE_MAP

COUNCIL_PAGE = 'http://www.chatham-kent.ca/Council/councilmembers/Pages/CouncilMembers.aspx'


class ChathamKentPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        wards = page.xpath('//table[@class="ms-rteTable-4"]')
        for ward in wards:
            district_info = ward.xpath('.//p')[0].text_content()
            if 'Mayor' in district_info:
                district = 'Chatham-Kent'
                role = 'Mayor'
            else:
                district = re.search(r'Ward \d+', district_info).group(0)
                role = 'Councillor'

            councillors = ward.xpath('.//a')
            for councillor in councillors:
                name = councillor.text_content()
                url = councillor.attrib['href']
                page = self.lxmlize(url)

                p = Person(primary_org='legislature', name=name, district=district, role=role)
                p.add_source(COUNCIL_PAGE)
                p.add_source(url)

                p.image = page.xpath('//div[@class="pageContent"]//img/@src')[0]

                address = page.xpath('//div[@id="div_contact_us_top_container_S"]//div[@class="div_contact_us_content_address"]')[0].text_content()
                p.add_contact('address', address, 'legislature')

                contacts = page.xpath('//div[@id="div_contact_us_top_container_S"]//div[@class="div_contact_us_content_kv"]/div')
                for contact in contacts:
                    contact_type, contact = contact.text_content().split(':')
                    contact_type = CONTACT_DETAIL_TYPE_MAP[contact_type.strip()]
                    p.add_contact(contact_type, contact.strip(), '' if contact_type == 'email' else 'legislature')
                yield p

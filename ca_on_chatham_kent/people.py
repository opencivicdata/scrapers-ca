from utils import CanadianScraper, CanadianPerson as Person, CONTACT_DETAIL_TYPE_MAP

import re
from collections import defaultdict

COUNCIL_PAGE = 'https://www.chatham-kent.ca/local-government/council/council-members'


class ChathamKentPersonScraper(CanadianScraper):
    def scrape(self):
        seat_numbers = defaultdict(int)
        voice_notes = ['legislature', 'office']

        page = self.lxmlize(COUNCIL_PAGE)

        wards = page.xpath('//div[@id="ctl00_PlaceHolderMain_ctl03__ControlWrapper_RichHtmlField"]//h4')
        assert len(wards), 'No wards found'
        for ward in wards:
            match = re.search(r'Ward \d+', ward.text_content())
            if match:
                area = match.group(0)
                role = 'Councillor'
                number = int(re.search(r'\((\d+)', ward.text_content()).group(1))
            else:
                area = 'Chatham-Kent'
                role = 'Mayor'
                number = 1

            councillors = ward.xpath('./following-sibling::*//a[contains(@href, "/Council/")]')[:number]
            assert len(councillors), 'No councillors found'
            for councillor in councillors:
                name = councillor.text_content()
                url = councillor.attrib['href']
                page = self.lxmlize(url)

                if role == 'Councillor':
                    seat_numbers[area] += 1
                    district = '{} (seat {})'.format(area, seat_numbers[area])
                else:
                    district = area

                p = Person(primary_org='legislature', name=name, district=district, role=role)
                p.add_source(COUNCIL_PAGE)
                p.add_source(url)

                image = page.xpath('//div[@id="ctl00_PlaceHolderMain_ctl03__ControlWrapper_RichHtmlField"]//img/@src')[0]
                if 'council_logo' not in image:
                    p.image = image

                address = page.xpath('//div[@id="div_contact_us_top_container_S"]//div[@class="div_contact_us_content_address"]')[0].text_content()
                p.add_contact('address', address, 'legislature')

                contacts = page.xpath('//div[@id="div_contact_us_top_container_S"]//div[@class="div_contact_us_content_kv"]/div')
                voice_note_index = 0
                for contact in contacts:
                    content = contact.text_content().strip()
                    if content:
                        contact_type, contact = contact.text_content().split(':')
                        contact_type = CONTACT_DETAIL_TYPE_MAP[contact_type.strip()]

                        if contact_type == 'voice':
                            note = voice_notes[voice_note_index]
                            voice_note_index += 1
                        elif contact_type == 'email':
                            note = ''
                        else:
                            note = 'legislature'

                        p.add_contact(contact_type, contact.strip(), note)

                yield p

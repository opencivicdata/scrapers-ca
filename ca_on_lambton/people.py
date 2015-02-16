from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

import re

COUNCIL_PAGE = 'http://www.lambtononline.ca/home/government/accessingcountycouncil/countycouncillors/Pages/default.aspx'


class LambtonPersonScraper(CanadianScraper):

    def scrape(self):
        councillor_seat_number = 1

        page = self.lxmlize(COUNCIL_PAGE)

        # Tableception here, first tr is left column, second the right column
        councillors_left = page.xpath('//div[@id="content"]/table/tr/td[1]/table/tr')
        councillors_right = page.xpath('//div[@id="content"]/table/tr/td[2]/table/tr')
        councillors = councillors_left + councillors_right
        for councillor in councillors:
            node = councillor.xpath('.//tr[1]')
            text = node[0].text_content()
            if 'Deputy Warden' in text:
                role = 'Deputy Warden'
                name = text.replace('Deputy Warden', '')
                district = 'Lambton'
            elif 'Warden' in text:
                role = 'Warden'
                name = text.replace('Warden', '')
                district = 'Lambton'
            else:
                role = 'Councillor'
                name = text
                district = 'Lambton (seat %d)' % councillor_seat_number
                councillor_seat_number += 1

            p = Person(primary_org='legislature', name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            p.image = councillor.xpath('.//img/@src')[0]

            info = councillor.xpath('./td/table/tr[2]/td')[0].text_content()
            residential_info = re.search('(?<=Residence:)(.*(?=Business Phone)|.*(?=Municipal Office))', info, flags=re.DOTALL).group(0)
            self.get_contacts(residential_info, 'residence', p)
            municipal_info = re.findall(r'(?<=Municipal Office:)(.*(?=Bio)|.*)', info, flags=re.DOTALL)[0]
            self.get_contacts(municipal_info, 'legislature', p)

            yield p

    def get_contacts(self, text, note, councillor):
        address = text.split('Telephone')[0].split('Phone')[0]
        councillor.add_contact('address', address, note)
        text = text.replace(address, '').split(':')
        for i, contact in enumerate(text):
            if i == 0:
                continue
            contact_type = next(x.strip() for x in re.findall(r'[A-Za-z ]+', text[i - 1]) if x.strip() and x.strip() != 'ext')
            if '@' in contact:
                contact = contact.strip()
            else:
                contact = re.findall(r'[0-9]{3}[- ][0-9]{3}-[0-9]{4}(?: ext\. [0-9]+)?', contact)[0].replace(' ', '-')

            if 'Fax' in contact_type:
                councillor.add_contact('fax', contact, note)
            elif 'Tel' in contact_type:
                councillor.add_contact('voice', contact, note)
            elif 'email' in contact_type:
                councillor.add_contact('email', contact)

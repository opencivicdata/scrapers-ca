from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

import re

COUNCIL_PAGE = 'http://www.richmondhill.ca/subpage.asp?pageid=townhall_members_of_the_council'


class RichmondHillPersonScraper(CanadianScraper):

    def scrape(self):
        regional_councillor_seat_number = 1

        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//center/center//a')
        for councillor in councillors:
            name = councillor.text_content().strip()
            url = councillor.attrib['href']
            page = self.lxmlize(url)
            header = page.xpath('//div[@class="sectionheading"]')[0].text_content()
            if header == 'Mayor of Richmond Hill':
                district = 'Richmond Hill'
                role = 'Mayor'
            else:
                district = re.findall(r',(.*)-', header)
                if district:
                    district = district[0].strip()
                else:
                    district = 'Richmond Hill (seat {})'.format(regional_councillor_seat_number)
                    regional_councillor_seat_number += 1

                role = 'Regional Councillor' if 'Regional' in header else 'Councillor'

            info = page.xpath('//table[@cellpadding>0]/tbody/tr/td[last()]|//table[not(@cellpadding)]/tbody/tr/td[last()]')
            info = info[0].text_content().replace(' - office:', ':')

            address = re.findall(r'(?<=Town of Richmond Hill)(.*(?=Telephone:)|(?=Telephone))', info)[0]
            address = re.sub(r'([a-z])([A-Z])', r'\1 \2', address)
            # I expected to be able to do '(.*)(?=\sTelephone|Telephone|Fax)', but nope.
            phone = re.findall(r'(?<=Telephone:) ((.*) (?=Telephone)|(.*)(?=Telephone)|(.*)(?=Fax))', info)[0][0].replace('(', '').replace(') ', '-').replace(', ext. ', ' x')
            fax = re.findall(r'(?<=Fax:) (.*)(?=E-mail)', info)[0].replace(' ', '').replace('(', '').replace(')', '-')
            email = self.get_email(page)

            p = Person(primary_org='legislature', name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)
            p.add_contact('address', address, 'legislature')
            p.add_contact('voice', phone, 'legislature')
            p.add_contact('fax', fax, 'legislature')
            p.add_contact('email', email)
            p.image = page.xpath('//img[contains(@alt, "{}")]/@src'.format(name))[0]
            if 'Website' in info:
                p.add_link(re.findall(r'www\..*\.[a-z]+', info)[0])
            yield p

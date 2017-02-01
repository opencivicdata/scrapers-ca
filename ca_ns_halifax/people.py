# coding: utf-8
from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

import re

COUNCIL_PAGE = 'http://www.halifax.ca/councillors/index.php'
MAYOR_PAGE = 'http://www.halifax.ca/mayor/'
MAYOR_CONTACT_URL = 'http://www.halifax.ca/mayor/contact.php'


class HalifaxPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        councillors = page.xpath('//div[./h2/a[contains(@href, "/District")]]')

        corrections = {
            'Timberlea—Beechville—Clayton Park—Wedgewood': 'Timberlea—Beechville—Clayton Park West',
        }

        for councillor in councillors:
            district = re.sub(r'\s*[–—-]\s*', '—', '—'.join(filter(None, (text.replace(',', '').strip() for text in councillor.xpath('./p/text()')))))
            district = corrections.get(district, district)

            name = councillor.xpath('./p/strong/text()')[0].replace('Councillor ', '').replace('Deputy Mayor ', '')

            if name != 'To be determined':
                photo = councillor.xpath('.//img/@src')[0]

                url = councillor.xpath('./h2/a/@href')[0]
                councillor_page = self.lxmlize(url)
                contact_details_url = councillor_page.xpath('//li/a[contains(@href, "contact")]/@href')[0]
                contact_page = self.lxmlize(contact_details_url)
                contact_node = contact_page.xpath('//div[./h1[contains(text(), "Contact")]]')[0]

                phone = self.get_phone(contact_node, area_codes=[902])
                email = self.get_email(contact_node)

                p = Person(primary_org='legislature', name=name, district=district, role='Councillor')
                p.add_source(COUNCIL_PAGE)
                p.add_source(contact_details_url)
                p.add_source(url)
                p.add_contact('voice', phone, 'legislature')
                p.add_contact('email', email)
                p.image = photo
                yield p

        mayor_page = self.lxmlize(MAYOR_PAGE, 'iso-8859-1')
        name = ' '.join(mayor_page.xpath('//h2[contains(., "Bio")]/text()')).strip()[:-len(' Bio')]
        contact_page = self.lxmlize(MAYOR_CONTACT_URL, 'iso-8859-1')
        email = self.get_email(contact_page)

        p = Person(primary_org='legislature', name=name, district='Halifax', role='Mayor')
        p.add_source(MAYOR_PAGE)
        p.add_source(MAYOR_CONTACT_URL)
        p.add_contact('email', email)
        yield p

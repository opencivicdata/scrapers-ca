from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

import re
from collections import defaultdict

from six.moves.urllib.parse import urljoin

COUNCIL_PAGE = 'http://www.woodbuffalo.ab.ca/Municipal-Government/Mayor-and-Council/Councillor-Profiles.htm'


class WoodBuffaloPersonScraper(CanadianScraper):

    def scrape(self):
        seat_numbers = defaultdict(int)

        page = self.lxmlize(COUNCIL_PAGE)

        mayor_url = page.xpath('//li[@id="pageid1075"]/div/a/@href')[0]
        yield self.scrape_mayor(mayor_url)

        wards = page.xpath('//b')
        for ward in wards:
            ward_name = ward.text_content()
            councillor_links = ward.xpath('./parent::p/a')
            for councillor_link in councillor_links:
                name = councillor_link.text

                if ward_name in ('Ward 1', 'Ward 2'):
                    seat_numbers[ward_name] += 1
                    district = '{} (seat {})'.format(ward_name, seat_numbers[ward_name])
                else:
                    district = ward_name

                p = Person(primary_org='legislature', name=name, district=district, role='Councillor')
                url = councillor_link.attrib['href']
                p.add_source(COUNCIL_PAGE)
                p.add_source(url)
                cpage = self.lxmlize(url)
                image_url_rel = cpage.xpath('//div[@id="content"]//img[contains(@alt, "Councillor")]/@src')[0]
                image_url = urljoin(url, image_url_rel)
                p.image = image_url

                contacts = page.xpath('//div[@id="content"]//div[@class="block"]/text()')
                for contact in contacts:
                    if not re.search(r'[0-9]', contact):
                        continue
                    if '(' not in contact:
                        contact_type = 'T'
                    else:
                        contact_type, contact = contact.split('(')
                    contact = contact.replace(') ', '-').strip()
                    if 'T' in contact_type:
                        p.add_contact('voice', contact, 'legislature')
                    if 'H' in contact_type:
                        p.add_contact('voice', contact, 'residence')
                    if 'C' in contact_type:
                        p.add_contact('cell', contact, 'legislature')
                    if 'F' in contact_type:
                        p.add_contact('fax', contact, 'legislature')
                email = self.get_email(cpage, '//div[@id="content"]//div[@class="block"]')
                p.add_contact('email', email)
                yield p

    def scrape_mayor(self, url):
        page = self.lxmlize(url)
        name = page.xpath('//h1[@id="pagetitle"]/text()')[0].replace('Mayor', '').strip()
        image = page.xpath('//div[@id="content"]/p[1]/img/@src')[0]
        contact_url = page.xpath('//li[@id="pageid1954"]/a/@href')[0]

        p = Person(primary_org='legislature', name=name, district='Wood Buffalo', role='Mayor')
        p.add_source(url)
        p.add_source(contact_url)
        p.image = image
        return p

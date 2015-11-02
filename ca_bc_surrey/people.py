from __future__ import unicode_literals
import re
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.surrey.ca/city-government/2999.aspx'


class SurreyPersonScraper(CanadianScraper):

    def scrape(self):
        councillor_seat_number = 1

        page = self.lxmlize(COUNCIL_PAGE)
        councillor_links = page.xpath('//div[@class="inner-wrapper"]//a[contains(text(), "Councillor")]')
        for link in councillor_links:
            role, name = link.text.split(' ', 1)
            url = link.attrib['href']
            councillor_page = self.lxmlize(url)

            district = 'Surrey (seat {})'.format(councillor_seat_number)
            councillor_seat_number += 1

            p = Person(primary_org='legislature', name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)

            contact_node = councillor_page.xpath('//div[@class="content"]//*[contains(text(), "Contact")]')
            if contact_node:
                phone = self.get_phone(councillor_page, area_codes=[604])
                email = self.get_email(councillor_page)
                p.add_contact('voice', phone, 'legislature')
                p.add_contact('email', email)

            photo_node = councillor_page.xpath('.//div[@class="inner-wrapper"]//img/@src')
            if photo_node:
                photo_url = photo_node[0]
                p.image = photo_url
            yield p

        mayor_link = page.xpath('//div[@class="inner-wrapper"]//a[contains(text(), "Mayor")]')[0]
        mayor_url = mayor_link.attrib['href']
        mayor_page = self.lxmlize(mayor_url)
        name_node = mayor_page.xpath('//div[@class="inner-wrapper"]//div[@class="inner-wrapper"]/p/text()')[0]
        name = re.search('([A-Z][a-z]+ [A-Z][a-z]+).', name_node).group(1)
        photo_url = mayor_page.xpath('//div[@class="inner-wrapper"]//img/@src')[0]
        contact_page = self.lxmlize(mayor_page.xpath('//a[contains(.,"Contact Mayor")]/@href')[0])

        p = Person(primary_org='legislature', name=name, district='Surrey', role='Mayor', image=photo_url)
        p.add_source(COUNCIL_PAGE)
        p.add_source(mayor_url)
        p.add_contact('voice', self.get_phone(contact_page, area_codes=[604]), 'legislature')
        p.add_contact('email', self.get_email(contact_page))
        yield p

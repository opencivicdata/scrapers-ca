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

            photo_node = councillor_page.xpath('.//div[@class="inner-wrapper"]//img/@src')
            if photo_node:
                photo_url = photo_node[0]
                phone = councillor_page.xpath('//text()[contains(., "hone:")][1]|//text()[contains(., "604-")]')[0]
                email = self.get_email(councillor_page)
                district = 'Surrey (seat %d)' % councillor_seat_number
                councillor_seat_number += 1

                p = Person(primary_org='legislature', name=name, district=district, role=role, image=photo_url)
                p.add_source(COUNCIL_PAGE)
                p.add_source(url)
                p.add_contact('voice', phone, 'legislature')
                p.add_contact('email', email)
            else:
                p = Person(primary_org='legislature', name=name, district=district, role=role)
                p.add_source(COUNCIL_PAGE)
                p.add_source(url)

            yield p

        mayor_link = page.xpath('//div[@class="inner-wrapper"]//a[contains(text(), "Mayor")]')[0]
        mayor_url = mayor_link.attrib['href']
        mayor_page = self.lxmlize(mayor_url)
        name_node = mayor_page.xpath('//div[@class="inner-wrapper"]//div[@class="inner-wrapper"]/p/text()')[0]
        name = re.search('([A-Z][a-z]+ [A-Z][a-z]+).', name_node).group(1)
        photo_url = mayor_page.xpath('//div[@class="inner-wrapper"]//img/@src')[0]
        phone = mayor_page.xpath('//text()[contains(., "Office:")]')[0]
        # no email

        p = Person(primary_org='legislature', name=name, district='Surrey', role='Mayor', image=photo_url)
        p.add_source(COUNCIL_PAGE)
        p.add_source(mayor_url)
        p.add_contact('voice', phone, 'legislature')
        yield p

from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.kelowna.ca/CM/Page159.aspx'
MAYOR_PAGE = 'http://www.kelowna.ca/CM/Page3677.aspx'


class KelownaPersonScraper(CanadianScraper):

    def scrape(self):
        yield self.scrape_mayor()

        councillor_seat_number = 1

        page = self.lxmlize(COUNCIL_PAGE)
        links = page.xpath('//ul/li/a[contains(text(), "Councillor")]')
        for link in links:
            role, name = link.text_content().replace('\xa0', ' ').split(' ', 1)
            url = link.attrib['href']
            page = self.lxmlize(url)
            photo_url = page.xpath('//img[contains(@alt, "Councillor")]/@src')[0]
            phone_node = page.xpath('//p[contains(text(), "Phone") or contains(text(), "Office")]')[0]
            phone = phone_node.text_content().split(':')[1]
            email = self.get_email(page)

            district = 'Kelowna (seat %d)' % councillor_seat_number
            councillor_seat_number += 1

            p = Person(primary_org='legislature', name=name, district=district, role=role, image=photo_url)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)
            p.add_contact('voice', phone, 'legislature')
            p.add_contact('email', email)
            yield p

    def scrape_mayor(self):
        page = self.lxmlize(MAYOR_PAGE)

        name_node = page.xpath('//h1[contains(text(), "Mayor")]')[0]
        role, name = name_node.text_content().replace('\xa0', ' ').split(' ', 1)
        photo_url = page.xpath('//img[contains(@alt, "Mayor")]/@src')[0]
        phone = page.xpath('//h2[contains(text(), "Contact")]/following::p/strong')[0].text_content()
        email = self.get_email(page)
        district = 'Kelowna'

        p = Person(primary_org='legislature', name=name, district=district, role=role, image=photo_url)
        p.add_source(MAYOR_PAGE)
        p.add_contact('voice', phone, 'legislature')
        p.add_contact('email', email)
        return p

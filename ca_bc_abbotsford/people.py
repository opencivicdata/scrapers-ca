from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.abbotsford.ca/city_hall/mayor_and_council/city_council.htm'
CONTACT_PAGE = 'http://www.abbotsford.ca/contact_us.htm'


class AbbotsfordPersonScraper(CanadianScraper):

    def scrape(self):
        councillor_seat_number = 1

        coun_page = self.lxmlize(COUNCIL_PAGE)
        contact_page = self.lxmlize(CONTACT_PAGE)
        councillors = coun_page.xpath('//div[@id="main-content"]//h3')
        contact_data = contact_page.xpath('//p[contains(./strong/text(), "Mayor & Council")]/following-sibling::table[1]//tr')[2:]

        assert len(councillors), 'No councillors found'
        assert len(councillors) == len(contact_data), 'Expected {}, got {}'.format(len(councillors), len(contact_data))
        for councillor, contact in zip(councillors, contact_data):
            text = councillor.text_content()
            if text.startswith('Councill'):
                role = 'Councillor'
                district = 'Abbotsford (seat {})'.format(councillor_seat_number)
                councillor_seat_number += 1
            else:
                role = 'Mayor'
                district = 'Abbotsford'
            name = text.split(' ', 1)[1]
            image = councillor.xpath('./img/@src')[0]
            phone = contact.xpath('./td[2]/text()')[0]
            fax = contact.xpath('./td[3]/text()')[0]

            p = Person(primary_org='legislature', name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(CONTACT_PAGE)
            p.image = image
            p.add_contact('voice', phone, 'legislature')
            p.add_contact('fax', fax, 'legislature')

            yield p

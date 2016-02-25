from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.whitby.ca/en/townhall/meetyourcouncil.asp'


class WhitbyPersonScraper(CanadianScraper):

    def scrape(self):
        regional_councillor_seat_number = 1
        page = self.lxmlize(COUNCIL_PAGE)

        yield self.scrape_mayor(page)

        councillor_nodes = page.xpath('//h3[contains(text(), "Councillors")]/following-sibling::p')[:-1]
        for councillor_node in councillor_nodes:
            text = ' '.join(councillor_node.xpath('./strong/text()'))
            if 'Vacant' in text:
                continue

            name, role_district = text.split(', ', 1)

            if 'Regional Councillor' in role_district:
                role = role_district
                district = 'Whitby (seat {})'.format(regional_councillor_seat_number)
                regional_councillor_seat_number += 1
            else:
                role, district = role_district.strip().split(', ')
                district = district.split(' (')[0]

            email = self.get_email(councillor_node)
            image = councillor_node.xpath('./img/@src')[0]
            p = Person(primary_org='legislature', name=name, district=district, role=role, image=image)
            p.add_source(COUNCIL_PAGE)
            p.add_contact('email', email)
            yield p

    def scrape_mayor(self, page):
        mayor_node = page.xpath('//p[strong[contains(text(), "Mayor")]]')[0]
        name = mayor_node.xpath('./strong')[0].text_content().replace(',', '')
        email = self.get_email(mayor_node)
        phone = page.xpath('//p[contains(text(), "Phone")]/text()')[0].split(':')[1]
        image = mayor_node.xpath('./preceding-sibling::img/@src')[0]
        p = Person(primary_org='legislature', name=name, district='Whitby', role='Mayor', image=image)
        p.add_source(COUNCIL_PAGE)
        p.add_contact('voice', phone, 'legislature')
        p.add_contact('email', email)
        return p

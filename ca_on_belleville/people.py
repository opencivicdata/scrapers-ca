from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

import re
from collections import defaultdict

COUNCIL_PAGE = 'http://www.belleville.ca/city-hall/page/city-council'


class BellevillePersonScraper(CanadianScraper):
    seat_numbers = defaultdict(int)

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        mayor_node = page.xpath('//div[@class="content-field"]/h3[contains(./text(), "Mayor")]/following-sibling::p[2]')[0]
        yield self.scrape_mayor(mayor_node)

        ward_elems = page.xpath('//h3[contains(text(), "Councillors")]')
        for ward_elem in ward_elems:
            ward = re.search(r'(Ward.+) Councillors', ward_elem.text).group(1)
            councillor_name_elems = ward_elem.xpath('./following-sibling::div[1]//strong')
            for name_elem in councillor_name_elems:
                self.seat_numbers[ward] += 1
                district = '{} (seat {})'.format(ward, self.seat_numbers[ward])
                yield self.person_from_elem(name_elem, district, 'Councillor')

    def person_from_elem(self, name_elem, district, role):
        name = name_elem.text_content()
        phone = name_elem.xpath('./following-sibling::text()[2]')[0].split(': ')[1]
        email = name_elem.xpath('./following-sibling::a//text()')[0]
        photo_url = name_elem.xpath('./preceding::img[1]/@src')[0]

        p = Person(primary_org='legislature', name=name, district=district, role=role, image=photo_url)
        p.add_source(COUNCIL_PAGE)
        p.add_contact('voice', phone, 'legislature')
        p.add_contact('email', email)
        return p

    def scrape_mayor(self, node):
        name = node.xpath('./strong/text()')[0]
        phone = node.xpath('./text()')[2].split(': ')[1]
        fax = node.xpath('./text()')[3].split(': ')[1]
        email = node.xpath('./a/text()')[0]
        photo_url = node.xpath('./preceding::p//img/@src')[0]

        p = Person(primary_org='legislature', name=name, district='Belleville', role='Mayor', image=photo_url)
        p.add_source(COUNCIL_PAGE)
        p.add_contact('voice', phone, 'legislature')
        p.add_contact('fax', fax, 'legislature')
        p.add_contact('email', email)
        return p

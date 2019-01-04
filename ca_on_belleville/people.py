from utils import CanadianScraper, CanadianPerson as Person

import re
from collections import defaultdict

COUNCIL_PAGE = 'http://www.belleville.ca/city-hall/page/city-council'


class BellevillePersonScraper(CanadianScraper):
    seat_numbers = defaultdict(int)

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        node = page.xpath('//div[@class="content-field"]/h3[contains(./text(), "Mayor")]/following-sibling::p[2]')[0]
        name = node.xpath('./strong/text()')[0]
        phone = node.xpath('./text()')[2].split(': ')[1]
        fax = node.xpath('./text()')[3].split(': ')[1]
        email = node.xpath('./a/text()')[0]
        image = node.xpath('./preceding::p//img/@src')[0]

        p = Person(primary_org='legislature', name=name, district='Belleville', role='Mayor')
        p.add_source(COUNCIL_PAGE)
        p.add_contact('voice', phone, 'legislature')
        p.add_contact('fax', fax, 'legislature')
        p.add_contact('email', email)
        p.image = image

        yield p

        wards = page.xpath('//h3[contains(text(), "Councillors")]')
        assert len(wards), 'No councillors found'
        for ward in wards:
            ward_name = re.search(r'(Ward.+) Councillors', ward.text).group(1)
            councillors = ward.xpath('./following-sibling::div[1]//strong')
            for councillor in councillors:
                self.seat_numbers[ward_name] += 1
                district = '{} (seat {})'.format(ward_name, self.seat_numbers[ward_name])
                role = 'Councillor'

                name = councillor.text_content()
                phone = councillor.xpath('./following-sibling::text()[2]')[0].split(':')[1]
                email = councillor.xpath('./following-sibling::a//text()')[0]
                image = councillor.xpath('./preceding::img[1]/@src')[0]

                p = Person(primary_org='legislature', name=name, district=district, role=role)
                p.add_source(COUNCIL_PAGE)
                p.add_contact('voice', phone, 'legislature')
                p.add_contact('email', email)
                p.image = image

                yield p

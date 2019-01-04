from utils import CanadianScraper, CanadianPerson as Person

import re

COUNCIL_PAGE = 'http://www.milton.ca/en/townhall/mayorandcouncil.asp?_mid_=5972'


class MiltonPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//table[@id="Table1table"]/tbody/tr')
        assert len(councillors), 'No councillors found'
        for i, councillor in enumerate(councillors):
            role_district = councillor.xpath('./td[2]/p/text()')[0].strip()
            if 'Mayor' in role_district:
                name = role_district.replace('Mayor and Regional Councillor', '')
                role = 'Mayor'
                district = 'Milton'
            else:
                name = councillor.xpath('./td[2]/p/text()')[1]
                role, district = re.split(r' (?=Ward)', role_district)
                if role == 'Town and Regional Councillor':
                    role = 'Regional Councillor'
                elif role == 'Town Councillor':
                    role = 'Councillor'

            p = Person(primary_org='legislature', name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            p.image = councillor.xpath('./td[1]/p//img/@src')[0]

            numbers = councillor.xpath('./td[3]/p[2]/text()')
            for number in numbers:
                num_type, number = number.split(':')
                number = number.replace(', ext ', ' x').strip()
                p.add_contact(num_type, number, num_type)

            yield p

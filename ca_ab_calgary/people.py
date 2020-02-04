from utils import CanadianScraper, CanadianPerson as Person

import re

COUNCIL_PAGE = 'http://www.calgary.ca/citycouncil/Pages/Councillors-and-Wards.aspx'
MAYOR_PAGE = 'http://calgarymayor.ca/contact'


class CalgaryPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//div[contains(@class, "plcards")]')
        assert len(councillors), 'No councillors found'
        for index, councillor in enumerate(councillors):
            h2 = councillor.xpath('.//h2')[0]
            name = h2.xpath('./text()')[0]

            district = h2.xpath('./following-sibling::div//text()')[0]
            role = 'Councillor'
            email = None
            if 'Mayor' in district:
                district = 'Calgary'
                role = 'Mayor'
                email = 'themayor@calgary.ca'

            p = Person(primary_org='legislature', name=name, district=district, role=role)
            style = councillor.xpath('.//div[contains(@class, "card-media")]//@style')[0]
            p.image = re.search(r'http[^)]+', style).group(0)
            if email:
                p.add_contact('email', email)
            p.add_source(COUNCIL_PAGE)
            yield p

from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

from six.moves.urllib.parse import urljoin

COUNCIL_PAGE = 'http://www.calgary.ca/citycouncil/Pages/Councillors-and-Wards.aspx'
MAYOR_PAGE = 'http://calgarymayor.ca/contact'


class CalgaryPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//div[contains(@class, "councillorwrapper")]')
        assert len(councillors), 'No councillors found'
        for index, councillor in enumerate(councillors):
            name = councillor.xpath('.//h4/text()')[0]
            district = councillor.xpath('.//h4/span/text()')[0]
            role = 'Councillor'
            email = None

            if not district and index == 0:
                district = 'Calgary'
                role = 'Mayor'
                email = 'themayor@calgary.ca'

            p = Person(primary_org='legislature', name=name, district=district, role=role)
            p.image = councillor.xpath('.//@src')[0]
            if email:
                p.add_contact('email', email)
            p.add_source(COUNCIL_PAGE)
            yield p

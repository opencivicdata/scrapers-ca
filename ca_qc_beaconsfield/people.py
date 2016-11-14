from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.beaconsfield.ca/fr/notre-ville/conseil-de-ville-et-districts-electoraux'


class BeaconsfieldPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//div[contains(@class, "items-row")]')
        assert len(councillors), 'No councillors found'
        for councillor in councillors:
            text = councillor.xpath('.//h2')[0].text_content().strip()
            if ',' not in text:
                continue

            name, role_and_district = text.split(', ', 1)
            if role_and_district == 'Maire':
                district = 'Beaconsfield'
                role = 'Maire'
            else:
                district = role_and_district.split(' - ', 1)[1]
                role = 'Conseiller'

            p = Person(primary_org='legislature', name=name, district=district, role=role)
            p.image = councillor.xpath('.//@src')[0]
            p.add_contact('email', self.get_email(councillor))
            p.add_contact('voice', self.get_phone(councillor, area_codes=[514]), 'legislature')
            p.add_source(COUNCIL_PAGE)
            yield p

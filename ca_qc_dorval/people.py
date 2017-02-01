from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.ville.dorval.qc.ca/en/democratic-life/municipal-council'


class DorvalPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//td/p[2]')
        assert len(councillors), 'No councillors found'
        for councillor in councillors:
            info = councillor.xpath('./strong/text()')

            # In case the name spans on 2 lines
            if len(info) > 2 and 'Councillor' not in info[1]:
                role, district = info[2].split('-')
                info = [info[0] + info[1], role, district]

            name = info[0]

            if 'Vacant' not in info:
                if len(info) < 3:
                    district = 'Dorval'
                    role = 'Maire'
                else:
                    district = info[2]
                    role = 'Conseiller'
                p = Person(primary_org='legislature', name=name, district=district, role=role)
                p.add_source(COUNCIL_PAGE)

                p.image = councillor.xpath('./preceding-sibling::p/img/@src')[0]

                email = self.get_email(councillor)
                p.add_contact('email', email)

                yield p

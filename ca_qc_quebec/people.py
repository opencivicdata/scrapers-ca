# coding: utf-8
from utils import CanadianScraper, CanadianPerson as Person

import re

COUNCIL_PAGE = 'https://www.ville.quebec.qc.ca/apropos/gouvernance/conseil-municipal/membres.aspx'


class QuebecPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        sections = page.xpath('//div[contains(@class, "membres-conseil-municipal")]')
        for section in sections:
            councillors = section.xpath('./div')
            assert len(councillors), 'No councillors found'
            for councillor in councillors:
                name = ' '.join(reversed(councillor.xpath('./h3/span/text()')))
                if 'vacant' in name:
                    continue

                header = section.xpath('./preceding-sibling::h2/text()')[-1]
                if 'Mairie' in header:
                    district = 'Québec'
                    role = 'Maire'
                else:
                    district = councillor.xpath('./p[@itemprop="jobTitle"]/a/text()')[0]
                    district = re.search(r'\ADistrict (?:de(?: la)?|du|des) ([\w —–-]+)', district, flags=re.U).group(1)
                    role = 'Conseiller'

                if district == 'Saules':
                    district = 'Les Saules'
                else:
                    district = re.sub(r'–', '—', district)  # n-dash, m-dash

                p = Person(primary_org='legislature', name=name, district=district, role=role)
                p.add_source(COUNCIL_PAGE)
                p.image = councillor.xpath('./figure//@src')[0]
                p.add_contact('voice', self.get_phone(councillor, area_codes=[418]), 'legislature')
                yield p

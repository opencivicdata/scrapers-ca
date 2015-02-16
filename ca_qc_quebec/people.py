# coding: utf-8
from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

import re

COUNCIL_PAGE = 'http://www.ville.quebec.qc.ca/apropos/vie_democratique/elus/conseil_municipal/membres.aspx'


class QuebecPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//div[contains(@class, "ligne")]')
        for councillor in councillors:

            name = ' '.join(councillor.xpath('.//h3')[0].text_content().strip().split(', ')[::-1])
            if 'vacant' in name:
                continue
            district = councillor.xpath('./preceding-sibling::h2/text()')[-1]
            if 'Mairie' in district:
                district = 'Québec'
                role = 'Maire'
            else:
                text = councillor.xpath('.//a[@target="_blank"]/text()')
                district = re.search('\ADistrict électoral (?:de|du|des) (.+) - ?\d+\Z', text[0].strip().replace('\xa0', ''), flags=re.U).group(1)
                role = 'Conseiller'

            if district == 'Monts':
                district = 'Les Monts'
            elif district == 'Plateau':
                district = 'Le Plateau'
            else:
                district = re.sub('–', '—', district)  # n-dash, m-dash
                district = re.sub('\Ala ', 'La ', district)

            p = Person(primary_org='legislature', name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.image = councillor.xpath('./p//img/@src')[0]

            phone = self.get_phone(councillor, [418])
            p.add_contact('voice', phone, 'legislature')
            yield p

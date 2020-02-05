# coding: utf-8
from utils import CanadianScraper, CanadianPerson as Person

import re

COUNCIL_PAGE = 'https://www.v3r.net/a-propos-de-la-ville/vie-democratique/conseil-municipal/maire-et-conseillers-municipaux'


class TroisRivieresPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        members = page.xpath('//div[@class="photos_conseillers"]//figure')
        assert len(members), 'No councillors found'

        for member in members:
            photo_url = member.xpath('.//a//img/@src')[0]
            url = member.xpath('.//figcaption//a/@href')[0]
            email = self.lxmlize(url).xpath(
                '//div[@class="content-page"]//a[starts-with(@href, "mailto:")]/@href')[0]

            email = re.sub('^mailto:', '', email)
            name, district = map(lambda x: x.strip(), member.xpath('.//figcaption//text()'))
            district = re.sub(r'\A(?:de|des|du) ', lambda match: match.group(0).lower(), district, flags=re.I)
            role = 'Conseiller'

            if 'Maire' in district:
                district = 'Trois-Rivières'
                role = 'Maire'

            p = Person(primary_org='legislature', name=name, district=district, role=role, image=photo_url)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)
            p.add_contact('email', email)
            yield p

# coding: utf-8
from utils import CanadianScraper, CanadianPerson as Person

import re

COUNCIL_PAGE = 'http://www.v3r.net/a-propos-de-la-ville/vie-democratique/conseil-municipal/conseillers-municipaux'

MAYOR_URL = 'http://www.v3r.net/a-propos-de-la-ville/vie-democratique/mairie'


class TroisRivieresPersonScraper(CanadianScraper):
    def scrape(self):
        # mayor first, can't find email
        page = self.lxmlize(MAYOR_URL)
        photo_url = page.xpath('//img[contains(@alt, "Maire")]//@src')[0]
        name = page.xpath('//img/@alt[contains(., "Maire")]')[0]
        assert len(name), "missing mayor's name"
        if 'suppleant' not in name:
            name = re.sub(r'Maire(sse suppleante)?', '', name, flags=re.I).strip()
            p = Person(primary_org='legislature', name=name, district='Trois-Rivières', role='Maire', image=photo_url)
            p.add_source(MAYOR_URL)
            yield p

        page = self.lxmlize(COUNCIL_PAGE)
        members = page.xpath('//div[@class="photos_conseillers"]//figure')
        assert len(members), 'No councillors found'

        for member in members:
            photo_url = member.xpath('.//a//img/@src')[0]
            url = member.xpath('.//figcaption//a/@href')[0]
            email = self.lxmlize(url).xpath(
                '//div[@class="content-page"]//a[starts-with(@href, "mailto:")]/@href')[0]

            email = re.sub('^mailto:', '', email)
            name, district = map(
                lambda x: x.strip(),
                member.xpath('.//figcaption//text()'))

            district = re.sub(r'\A(?:de|des|du) ', lambda match: match.group(0).lower(), district, flags=re.I)

            p = Person(primary_org='legislature', name=name, district=district, role='Conseiller', image=photo_url)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)
            p.add_contact('email', email)
            yield p

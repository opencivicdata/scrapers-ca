# coding: utf-8
from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

import re

from six.moves.urllib.parse import urljoin

COUNCIL_PAGE = 'http://laville.v3r.net/portail/index.aspx?sect=0&module=5&module2=1&MenuID=150&CPage=1'

MAYOR_URL = 'http://laville.v3r.net/portail/index.aspx?sect=0&module=5&module2=1&MenuID=1&CPage=1'


class TroisRivieresPersonScraper(CanadianScraper):

    def scrape(self):
        # mayor first, can't find email
        page = self.lxmlize(MAYOR_URL)
        photo_url = page.xpath('//img/@src[contains(., "maire")]')[0]
        name = page.xpath('//td[@class="contenu"]/text()[last()]')[0]
        p = Person(primary_org='legislature', name=name, district="Trois-Rivières", role="Maire",
                   image=photo_url)
        p.add_source(MAYOR_URL)
        yield p

        resp = self.get(COUNCIL_PAGE)
        # page rendering through JS on the client
        page_re = re.compile(r'createItemNiv3.+"District (.+?)".+(index.+)\\"')
        for district, url_rel in page_re.findall(resp.text):
            if district not in ('des Estacades', 'des Plateaux', 'des Terrasses', 'du Sanctuaire'):
                district = re.sub('\A(?:de(?: la)?|des|du) ', '', district)

            url = urljoin(COUNCIL_PAGE, url_rel)
            page = self.lxmlize(url)

            name_content = page.xpath('//h2//text()')
            if name_content:
                name = name_content[0]
                email = self.get_email(page)
                photo_url = page.xpath('//img/@src[contains(., "Conseiller")]')[0]
                p = Person(primary_org='legislature', name=name, district=district, role='Conseiller',
                           image=photo_url)
                p.add_source(url)
                p.add_contact('email', email)
                yield p

# coding: utf-8
from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

import re
from six.moves.urllib.parse import urljoin

COUNCIL_PAGE = 'http://www.cotesaintluc.org/Administration'


class CoteSaintLucPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        mayor_url = page.xpath('//a[contains(text(), "Mayor")]/@href')[0]
        mayor = self.scrape_mayor(mayor_url)
        if mayor:
            yield mayor

        councillors_url = page.xpath('//a[contains(text(), "Councillors")]/@href')[0]
        cpage = self.lxmlize(councillors_url)

        councillor_rows = cpage.xpath('//tr[td//img]')[:-1]
        for councillor_row in councillor_rows:
            img_cell, info_cell = tuple(councillor_row)
            if info_cell.xpath('.//p//text()[contains(., "Vacant")]'):
                continue
            cells = [x.strip() for x in info_cell.xpath('.//text()') if re.sub('\xa0', ' ', x).strip()]
            name = cells[0].replace('Councillor ', '')
            district = info_cell.xpath('.//p[contains(text(), "District")]//text()')[0]
            email = self.get_email(info_cell)
            phone = self.get_phone(info_cell, area_codes=[438, 514], error=False)
            img_url_rel = img_cell.xpath('.//img/@src')[0]
            img_url = urljoin(councillors_url, img_url_rel)

            p = Person(primary_org='legislature', name=name, district=district, role='Conseiller')
            p.add_source(COUNCIL_PAGE)
            p.add_source(councillors_url)
            p.add_contact('email', email)
            if phone:
                p.add_contact('voice', phone, 'legislature')
            p.image = img_url
            yield p

    def scrape_mayor(self, url):
        page = self.lxmlize(url)
        text = page.xpath('//h1//text()[contains(., "Mayor")]')[0]
        if 'Acting Mayor' in text:
            # A councillor is acting mayor. We would need to add two roles to
            # the same person, which can be done with a little effort.
            return

        name = re.sub('(?:Acting )?Mayor ', '', text)

        email = self.get_email(page)
        phone = self.get_phone(page.xpath('//table[1]')[0])

        p = Person(primary_org='legislature', name=name, district='Côte-Saint-Luc', role='Maire')
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)
        p.image = page.xpath('.//div[contains(@class,"content")]//img/@src')[0]
        p.add_source(url)
        p.add_contact('email', email)
        p.add_contact('voice', phone, 'legislature')
        return p

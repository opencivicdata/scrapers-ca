# coding: utf-8
from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

from six.moves.urllib.parse import urljoin

COUNCIL_PAGE = 'http://www.cotesaintluc.org/Administration'


class CoteSaintLucPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        mayor_url = page.xpath('//a[contains(text(), "Mayor")]/@href')[0]
        yield self.scrape_mayor(mayor_url)

        councillors_url = page.xpath('//a[contains(text(), "Councillors")]/@href')[0]
        cpage = self.lxmlize(councillors_url)

        councillor_rows = cpage.xpath('//tr[td//img]')[:-1]
        for councillor_row in councillor_rows:
            img_cell, info_cell = tuple(councillor_row)
            name = info_cell.xpath('.//span//text()[contains(., "Councillor")]')[0][len('Councillor '):]
            district = info_cell.xpath('.//p[contains(text(), "District")]//text()')[0]
            email = self.get_email(info_cell)
            phone = self.get_phone(info_cell, [438, 514])
            img_url_rel = img_cell.xpath('.//img/@src')[0]
            img_url = urljoin(councillors_url, img_url_rel)

            p = Person(primary_org='legislature', name=name, district=district, role='Conseiller')
            p.add_source(COUNCIL_PAGE)
            p.add_source(councillors_url)
            p.add_contact('email', email)
            p.add_contact('voice', phone, 'legislature')
            p.image = img_url
            yield p

    def scrape_mayor(self, url):
        page = self.lxmlize(url)
        name = page.xpath('//span//text()[contains(., "Mayor")]')[0][len('Mayor '):]

        email = self.get_email(page)
        phone = page.xpath('//table[1]/tbody/tr/td[1]/p[last()]/text()')[2].replace('Telephone: ', '')

        p = Person(primary_org='legislature', name=name, district='Côte-Saint-Luc', role='Maire')
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)
        p.image = page.xpath('.//img/@src')[0]
        p.add_source(url)
        p.add_contact('email', email)
        p.add_contact('voice', phone, 'legislature')
        return p

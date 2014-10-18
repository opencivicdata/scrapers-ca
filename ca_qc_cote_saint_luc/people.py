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
            name = info_cell.xpath(
                'string(.//span[contains(text(), "Councillor")])')[len('Councillor '):]
            district = info_cell.xpath('string(.//p[contains(text(), "District")])')
            email = info_cell.xpath('string(.//a[contains(@href, "mailto:")])')
            if not email:
                email = info_cell.xpath('string(.//strong[contains(text(), "E-mail")]/following-sibling::text())')
            phone = info_cell.xpath(
                'string(.//p[contains(.//text(), "Telephone:")])').split(':')[1]
            img_url_rel = img_cell.xpath('string(//img/@href)')
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
        name = page.xpath(
            'string(//span[contains(text(), "Mayor")])')[len('Mayor '):]

        email = page.xpath('.//a[contains(@href, "mailto:")]/text()')[0]
        phone = page.xpath('//table[1]/tbody/tr/td[1]/p[last()]/text()')[2].replace('Telephone: ', '')

        p = Person(primary_org='legislature', name=name, district='Côte-Saint-Luc', role='Maire')
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)
        p.image = page.xpath('.//img/@src')[0]
        p.add_source(url)
        p.add_contact('email', email)
        p.add_contact('voice', phone, 'legislature')
        return p

from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

import re

COUNCIL_PAGE = 'https://www.longueuil.quebec/fr/conseil-ville'


class LongueuilPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, 'utf-8')

        yield self.scrape_mayor(page)

        for tr in page.xpath('//tbody/tr'):
            if tr.xpath('./td[2]//text()')[0] != 'Vacant':
                district = tr.xpath('./td[1]/text()')[0]
                if 'Conseiller n' in district:
                    district = 'Greenfield Park'
                detail_url = tr.xpath('./td[2]/a/@href')[0]
                detail_page = self.lxmlize(detail_url, 'utf-8')

                name = detail_page.xpath('//h1/text()')[0]
                photo_node = detail_page.xpath('//img[contains(@alt, "{0}")]/@src'.format(name))
                if photo_node:
                    photo_url = photo_node[0]
                else:
                    photo_url = detail_page.xpath('//img[contains(@class, "droite")]/@src')[0]

                p = Person(primary_org='legislature', name=name, district=district, role='Conseiller')
                p.add_source(COUNCIL_PAGE)
                p.add_source(detail_url)
                p.image = photo_url
                yield p

    def scrape_mayor(self, page):
        mayor_node = page.xpath('//a[contains(@href, "maire")]/ancestor::strong')[0]
        name, position = [string.title() for string in mayor_node.text_content().split(', ')]
        mayor_url = mayor_node.xpath('.//a/@href')[0]
        mayor_page = self.lxmlize(mayor_url)
        photo_url = mayor_page.xpath('//img[contains(@alt, "{0}")]/@src'.format(name))[0]
        p = Person(primary_org='legislature', name=name, district='Longueuil', role='Maire')
        p.add_source(COUNCIL_PAGE)
        p.add_source(mayor_url)
        p.image = photo_url
        yield p

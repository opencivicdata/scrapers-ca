from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

import re

COUNCIL_PAGE = 'http://www.longueuil.ca/fr/conseil-ville'


class LongueuilPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, 'latin-1')
        person_rows = [tr for tr in page.xpath('//tr') if
                       tr.xpath('./td[2][@class="TABL1"]')]
        leader_row = person_rows[0]
        councillor_rows = person_rows[1:]
        for row in councillor_rows:
            district = row[1].text if row[1].text.strip() else 'Greenfield Park'
            name = row[2].xpath('string(./a)').title()
            detail_url = row[2].xpath('./a/@href')[0]
            detail_page = self.lxmlize(detail_url)
            email_url = detail_page.xpath(
                '//a[contains(@href, "sendto")]/@href')[0]
            email = re.search(r'sendto=(.+)&', email_url).group(1)
            photo_url = detail_page.xpath('//img[@height="200"]/@src')[0]
            p = Person(primary_org='legislature', name=name, district=district, role='Conseiller')
            p.add_source(COUNCIL_PAGE)
            p.add_source(detail_url)
            p.image = photo_url
            p.add_contact('email', email)
            yield p

        mayor_td = leader_row[1]
        name, position = [string.title() for string in
                          mayor_td.text_content().split(', ')]
        mayor_url = mayor_td.xpath('.//a/@href')[0]
        mayor_page = self.lxmlize(mayor_url)
        photo_url = mayor_page.xpath('//b/img/@src')[0]
        email_url = detail_page.xpath(
            '//a[contains(@href, "sendto")]/@href')[0]
        email = re.search(r'sendto=(.+)&', email_url).group(1)
        p = Person(primary_org='legislature', name=name, district='Longueuil', role='Maire')
        p.add_source(COUNCIL_PAGE)
        p.add_source(mayor_url)
        p.image = photo_url
        p.add_contact('email', email)
        yield p

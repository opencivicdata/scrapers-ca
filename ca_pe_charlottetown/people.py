# coding: utf-8
from __future__ import unicode_literals

import re

from six.moves.urllib.parse import urljoin

from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.city.charlottetown.pe.ca/mayorandcouncil.php'


class CharlottetownPersonScraper(CanadianScraper):

    def scrape(self):
        root = self.lxmlize(COUNCIL_PAGE)
        everyone = root.xpath('//span[@class="Title"]')
        mayornode = everyone[0]
        mayor = {}
        spantext = ' '.join(mayornode.xpath('.//text()'))
        mayor['name'] = re.search(r'[^(]+', spantext).group(0).strip()
        mayor['photo_url'] = urljoin(COUNCIL_PAGE, mayornode.xpath('img/@src')[0])
        mayor['email'] = mayornode.xpath('following::a[1]/text()')[0]

        m = Person(primary_org='legislature', name=mayor['name'], district='Charlottetown', role='Mayor')
        m.add_source(COUNCIL_PAGE)
        m.add_contact('email', mayor['email'])
        m.image = mayor['photo_url']

        yield m

        for span in root.xpath('//span[@class="Title"]')[1:]:
            spantext = ' '.join(span.xpath('.//text()'))
            header = spantext.replace('\u2013', '-').split('-')
            if len(header) != 2:
                continue

            name = header[0].strip()
            name = name.replace('Councillor', '')
            name = re.sub(r'\(.+?\)', '', name)
            name = ' '.join(name.split())

            district_id = ' '.join(header[1].split()[:2])

            # needed a wacky xpath to deal with ward 8
            photo = span.xpath('preceding::hr[1]/following::img[1]/@src')
            photo_url = urljoin(COUNCIL_PAGE, photo[0])

            email = span.xpath('string(following::a[1]/text())')

            p = Person(primary_org='legislature', name=name, district=district_id, role='Councillor')
            p.add_source(COUNCIL_PAGE)
            if email:
                p.add_contact('email', email)
            p.image = photo_url

            yield p

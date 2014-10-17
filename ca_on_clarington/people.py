from __future__ import unicode_literals

import re

from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.clarington.net/index.php?content=townhall/council'


class ClaringtonPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        for person_header_elem in page.xpath('//h2'):
            role, name_post = person_header_elem.text.split(' - ')
            try:
                name, caps_post = re.match(r'(.+) \((.+)\)', name_post).groups()
                post = caps_post.title()
            except AttributeError:
                name = name_post
                post = "Clarington"
            email = person_header_elem.xpath(
                'string(./following-sibling::a[1]/@href)')[len('mailto:'):]
            photo_url = person_header_elem.xpath(
                'string(./following-sibling::img[1]/@src)')
            p = Person(primary_org='legislature', name=name, district=post, role=role, image=photo_url)
            p.add_source(COUNCIL_PAGE)
            p.add_contact('email', email)
            yield p

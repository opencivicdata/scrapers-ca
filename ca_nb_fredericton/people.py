from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

import re

COUNCIL_PAGE = 'http://www.fredericton.ca/en/citygovernment/CityCouncil.asp'


class FrederictonPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//table/tbody/tr')
        for councillor in councillors:
            if not councillor.text_content() or 'Remembering' in councillor.text_content():
                continue

            text = councillor.xpath('.//strong/text()')[0]
            name = text.split(',')[0].replace('Name:', '').replace('\x92', "'").strip()
            if 'Mayor' in text and 'Deputy Mayor' not in text:
                role = 'Mayor'
                district = 'Fredericton'
            else:
                district = re.search(r'Ward \d+', councillor.text_content()).group(0)
                role = 'Councillor'

            p = Person(primary_org='legislature', name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            p.image = councillor.xpath('.//img/@src')[0]

            yield p

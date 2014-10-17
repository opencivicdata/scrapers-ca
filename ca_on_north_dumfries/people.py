from __future__ import unicode_literals
from pupa.scrape import Scraper

import re

from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.northdumfries.ca/en/ourtownship/MeetYourCouncil.asp'


class NorthDumfriesPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//table/tbody/tr')[1:]
        for councillor in councillors:
            info = councillor.xpath('./td//text()')
            info = [x for x in info if x.strip()]
            name = info.pop(0).replace('Councillor', '')
            if 'Mayor' in name:
                district = 'North Dumfries'
                name = name.replace('Mayor', '').strip()
                role = 'Mayor'
            else:
                district = 'Ward %s' % info.pop(0).strip()
                role = 'Councillor'
            p = Person(primary_org='legislature', name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_contact('voice', info[0], 'legislature')
            p.add_contact('email', info[1])
            yield p

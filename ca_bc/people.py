from __future__ import unicode_literals
from pupa.scrape import Scraper

import re

from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.leg.bc.ca/mla/3-2.htm'


class BritishColumbiaPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//table[@cellpadding="3"]//td//a/@href')
        for councillor in councillors:
            page = self.lxmlize(councillor)
            name = page.xpath('//b[contains(text(), "MLA:")]')[0].text_content().replace('MLA:', '').replace('Hon.', '').replace(', Q.C.', '').strip()
            district = page.xpath('//em/strong/text()')[0].strip()

            party_caps = page.xpath('string((//table[@width=440]//b)[last()])')
            party = party_caps.strip().title().replace('Of', 'of')
            p = Person(primary_org='legislature', name=name, district=district, role='MLA', party=party)
            p.add_source(COUNCIL_PAGE)
            p.add_source(councillor)

            p.image = page.xpath('//a[contains(@href, "images/members")]/@href')[0]

            email = page.xpath('//a[contains(@href, "mailto:")]/text()')[0]
            p.add_contact('email', email)

            office = ', '.join(page.xpath('//i/b[contains(text(), "Office:")]/ancestor::p/text()'))
            office = re.sub(r'\s{2,}', ' ', office)
            p.add_contact('address', office, 'legislature')

            constituency = page.xpath('//i/b[contains(text(), "Constituency:")]/ancestor::p/text()')
            if not 'TBD' in constituency[0]:
                constituency = re.sub(r'\s{2,}', ' ', ', '.join(constituency))
                p.add_contact('address', constituency, 'constituency')

            phones = page.xpath('//strong[contains(text(), "Phone:")]/ancestor::tr[1]')[0]
            office_phone = phones.xpath('./td[2]//text()')[0].strip().replace(' ', '-')
            p.add_contact('voice', office_phone, 'legislature')
            constituency_phone = phones.xpath('./td[4]//text()')[0].strip().replace(' ', '-')
            if not 'TBD' in constituency_phone:
                p.add_contact('voice', constituency_phone, 'constituency')

            faxes = page.xpath('//strong[contains(text(), "Fax:")]/ancestor::tr[1]')[0]
            office_fax = faxes.xpath('./td[2]//text()')[0].strip().replace(' ', '-')
            p.add_contact('fax', office_fax, 'legislature')
            constituency_fax = faxes.xpath('./td[4]//text()')[0].strip().replace(' ', '-')
            if not 'TBD' in constituency_fax:
                p.add_contact('fax', constituency_fax, 'constituency')
            yield p

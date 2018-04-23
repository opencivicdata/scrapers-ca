# coding: utf-8
from utils import CanadianScraper, CanadianPerson as Person

import re

COUNCIL_PAGE = 'http://www.assembly.nl.ca/js/members-index.js'

PARTIES = {
    'Progressive Conservative': 'Progressive Conservative Party of Newfoundland and Labrador',
    'New Democrat': 'New Democratic Party of Newfoundland and Labrador',
    'Liberal': 'Liberal Party of Newfoundland and Labrador',
    'Independent/Non-Affiliated': 'Independent',
}

PHONE_TD_HEADINGS = {
    'legislature': "Confederation Building Office",
    'constituency': "Constituency Office",
}


class NewfoundlandAndLabradorPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.get(COUNCIL_PAGE)
        members = re.findall('/Members/YourMember/[^"]+', page.text)
        assert len(members), 'No members found'
        for member in members:
            detail_url = 'http://www.assembly.nl.ca%s' % member
            detail = self.lxmlize(detail_url)

            name = detail.xpath('//h1/text()')[0]
            district = re.sub(r' [\xa0–-] ', '—', detail.xpath('//h2/text()')[0])  # # n-dash, m-dash
            party = PARTIES[detail.xpath('//h3/text()')[0]]

            p = Person(primary_org='legislature', name=name, district=district, role='MHA', party=party)
            p.image = detail.xpath('//img[@class="img-responsive"]/@src')[0]

            contact = detail.xpath('//div[@class="col-md-12"]')[0]
            p.add_contact('email', self.get_email(contact))

            p.add_source(COUNCIL_PAGE)
            p.add_source(detail_url)

            for key, heading in PHONE_TD_HEADINGS.items():
                node = detail.xpath('//*[.="{0}"]/ancestor::div'.format(heading))
                if node:
                    phone = self.get_phone(node[0], area_codes=[709])
                    if phone:
                        p.add_contact('voice', phone, key)

            yield p

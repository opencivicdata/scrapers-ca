# coding: utf-8
from utils import CanadianScraper, CanadianPerson as Person, CUSTOM_USER_AGENT

import re

COUNCIL_PAGE = 'http://www.assembly.nl.ca/js/members-index.js'

PARTIES = {
    'Progressive Conservative': 'Progressive Conservative Party of Newfoundland and Labrador',
    'New Democrat': 'New Democratic Party of Newfoundland and Labrador',
    'Liberal': 'Liberal Party of Newfoundland and Labrador',
    'Independent/Non-Affiliated': 'Independent',
}

HEADING_TYPE = {
    'Confederation Building Office:': 'legislature',
    'Constituency Office:': 'constituency',
}


class NewfoundlandAndLabradorPersonScraper(CanadianScraper):
    def scrape(self):
        self.user_agent = CUSTOM_USER_AGENT
        page = self.get(COUNCIL_PAGE)
        members = re.findall('/Members/YourMember/[^"]+', page.text)
        assert len(members), 'No members found'
        for member in members:
            detail_url = 'http://www.assembly.nl.ca%s' % member
            detail = self.lxmlize(detail_url, user_agent=CUSTOM_USER_AGENT)

            name = detail.xpath('//h1/text()')[0]
            district = re.sub(r' [\xa0–-] ', '—', detail.xpath('//h2/text()')[0])  # # n-dash, m-dash
            party = PARTIES[detail.xpath('//h3/text()')[0]]

            p = Person(primary_org='legislature', name=name, district=district, role='MHA', party=party)
            p.image = detail.xpath('//img[@class="img-responsive"]/@src')[0]

            contact = detail.xpath('//div[@class="col-md-12"]')[0]
            p.add_contact('email', self.get_email(contact))

            p.add_source(COUNCIL_PAGE)
            p.add_source(detail_url)

            for heading, _type in HEADING_TYPE.items():
                node = detail.xpath('//b[.="%s"]/../..' % heading)
                if node:
                    phone = self.get_phone(node[0], error=False)
                    if phone:
                        p.add_contact('voice', phone, _type)

            yield p

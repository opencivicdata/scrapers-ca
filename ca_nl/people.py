# coding: utf-8
from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.assembly.nl.ca/members/cms/membersdirectlines.htm'
PARTY_PAGE = 'http://www.assembly.nl.ca/members/cms/membersparty.htm'

PARTIES = [
    'Progressive Conservative Party of Newfoundland and Labrador',
    'New Democratic Party of Newfoundland and Labrador',
    'Liberal Party of Newfoundland and Labrador',
]

PHONE_TD_HEADINGS = {
    'legislature': "Confederation Building Office",
    'constituency': "Constituency Office",
}


def get_party(abbr):
    """Return a full party name from an abbreviation"""
    return next((party for party in PARTIES if party[0] == abbr[0]), None)


class NewfoundlandAndLabradorPersonScraper(CanadianScraper):

    def scrape(self):
        member_parties = {}
        for elem in self.lxmlize(PARTY_PAGE).xpath('//h3/u'):
            party = elem.text
            members = elem.xpath('./ancestor::tr/following-sibling::tr/td')
            member_names = [elem.text_content().replace('\xa0', ' ') for elem in members]
            for name in member_names:
                member_parties[name] = party

        page = self.lxmlize(COUNCIL_PAGE)
        for row in page.xpath('//table[not(@id="footer")][not(@style)]/tr')[1:]:
            name, district, _, email = [cell.text_content().replace('\xa0', ' ') for cell in row]

            district = district.replace(' - ', '—')  # m-dash
            district = district.replace('Bay De Verde', 'Bay de Verde')
            party = get_party(member_parties[name.strip()])

            p = Person(primary_org='legislature', name=name, district=district, role='MHA', party=party)

            p.add_contact('email', email)

            text = row[2].xpath('./text()')
            if text and text[0].strip():
                p.add_contact('voice', text[0], 'legislature')

            p.add_source(COUNCIL_PAGE)
            p.add_source(PARTY_PAGE)

            photo_page_url = row[0].xpath('./a/@href')
            if photo_page_url:
                photo_page = self.lxmlize(photo_page_url[0])
                photo_node = photo_page.xpath('//table//img/@src')
                photo_url = photo_node[0]
                p.image = photo_url
                p.add_source(photo_page_url[0])
                for key, heading in PHONE_TD_HEADINGS.items():
                    try:
                        td = photo_page.xpath(
                            '//*[.="{0}"]/ancestor::td'.format(
                                heading
                            )
                        )[0]
                    except IndexError:
                        pass  # no match found for heading
                    else:
                        phone = self.get_phone(td, error=False)
                        if phone:
                            p.add_contact('voice', phone, key)

            yield p

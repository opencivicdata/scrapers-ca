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


def get_party(abbr):
    """Return a full party name from an abbreviation"""
    return next((party for party in PARTIES if party[0] == abbr[0]), None)


class NewfoundlandAndLabradorPersonScraper(CanadianScraper):

    def scrape(self):
        member_parties = dict(process_parties(self.lxmlize(PARTY_PAGE)))

        page = self.lxmlize(COUNCIL_PAGE)
        for row in page.xpath('//table[not(@id="footer")]/tr')[1:]:
            try:
                name, district, _, email = [
                    cell.xpath('string(.)').replace('\xa0', ' ') for cell in row]
                email = email.split()[0]
            except ValueError:
                continue
            phone = row[2].xpath('text()[1]')[0]
            try:
                photo_page_url = row[0].xpath('./a/@href')[0]
            except IndexError:
                continue  # there is a vacant district
            photo_page = self.lxmlize(photo_page_url)
            photo_url = photo_page.xpath('//table//img/@src')[0]
            district = district.replace(' - ', '—')  # m-dash
            party = get_party(member_parties[name.strip()])
            p = Person(primary_org='legislature', name=name, district=district, role='MHA',
                       party=party, image=photo_url)
            p.add_source(COUNCIL_PAGE)
            p.add_source(PARTY_PAGE)
            p.add_source(photo_page_url)
            p.add_contact('email', email)
            # TODO: either fix phone regex or tweak phone value
            p.add_contact('voice', phone, 'legislature')
            yield p


def process_parties(partypage):
    # return generator of (name, party) tuples for MHAs
    for elem in partypage.xpath('//h3/u'):
        party = elem.text
        members = elem.xpath('./ancestor::tr/following-sibling::tr/td/a')
        member_names = [elem.text.replace('\xa0', ' ') for elem in members]
        for name in member_names:
            yield (name, party)

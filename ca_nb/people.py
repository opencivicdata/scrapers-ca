from utils import CanadianScraper, CanadianPerson as Person

import re
from urllib.parse import urljoin

COUNCIL_PAGE = 'http://www1.gnb.ca/legis/bios/58/index-e.asp'

PARTIES = {
    'PC': 'Progressive Conservative Party of New Brunswick',
    'L': 'New Brunswick Liberal Association',
    'IND': 'Independent',
    'GP': 'Green Party'
}


def get_party(abbr):
    """Return full party name based on abbreviation"""
    return PARTIES[abbr]


class NewBrunswickPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        councillor_table = page.xpath('//table[@id="customers"]')[0]
        members = councillor_table.xpath('.//tr')[1:]
        assert len(members), 'No members found'
        for row in members:
            riding, table_name, email = (' '.join(td.text_content().split()) for td in row[1:])

            if 'Vacant' in table_name:
                continue

            district = riding.replace('\x97', '-')
            name_with_status, party_abbr = re.match(r'(.+) \((.+)\)', table_name).groups()
            name = name_with_status.split(',')[0]
            photo_page_url = row[2][0].attrib['href']
            photo_url = self.get_photo_url(photo_page_url)

            # @see https://en.wikipedia.org/wiki/Charlotte-Campobello
            if district == 'Saint Croix':
                district = 'Charlotte-Campobello'
            # @see https://en.wikipedia.org/wiki/Oromocto-Lincoln-Fredericton
            elif district == 'Oromocto-Lincoln-Fredericton':
                district = 'Oromocto-Lincoln'

            p = Person(primary_org='legislature', name=name, district=district, role='MLA',
                       party=get_party(party_abbr.strip()), image=photo_url)
            p.add_contact('email', email)
            p.add_source(photo_page_url)
            p.add_source(COUNCIL_PAGE)
            yield p

    def get_photo_url(self, url):
        page = self.lxmlize(url)
        rel = page.xpath('//td/img/@src')[0]
        return urljoin(url, rel)

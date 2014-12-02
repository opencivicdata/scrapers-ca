from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

import re

from six.moves.urllib.parse import urljoin

COUNCIL_PAGE = 'http://www1.gnb.ca/legis/bios1/index-e.asp'

PARTIES = {
    'PC': 'Progressive Conservative Party of New Brunswick',
    'L': 'New Brunswick Liberal Association',
    'IND': 'Independent'
}


def get_party(abbr):
    """Return full party name based on abbreviation"""
    return PARTIES[abbr]


class NewBrunswickPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        councillor_table = page.xpath('//body/div[2]/table[2]')[0]
        for row in councillor_table.xpath('.//tr'):
            riding, table_name, email = (' '.join(td.text_content().split()) for td in row[1:])
            riding_fixed = riding.replace('\x97', '-')
            if riding_fixed == 'Miramichi Bay-Neguac':
                riding_fixed = 'Miramichi-Bay-Neguac'
            name_with_status, party_abbr = re.match(
                r'(.+) \((.+)\)', table_name).groups()
            name = name_with_status.split(',')[0]
            photo_page_url = row[2][0].attrib['href']
            photo_url = self.get_photo_url(photo_page_url)

            p = Person(primary_org='legislature', name=name, district=riding_fixed, role='MLA',
                       party=get_party(party_abbr), image=photo_url)
            p.add_contact('email', email)
            p.add_source(photo_page_url)
            p.add_source(COUNCIL_PAGE)
            yield p

    def get_photo_url(self, url):
        page = self.lxmlize(url)
        rel = page.xpath('//td/img/@src')[0]
        return urljoin(url, rel)

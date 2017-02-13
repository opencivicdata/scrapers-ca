from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.gov.mb.ca/legislature/members/mla_list_alphabetical.html'


def get_party(abbreviation):
    return {
        'NDP': 'New Democratic Party of Manitoba',
        'PC': 'Progressive Conservative Party of Manitoba',
        'L': 'Manitoba Liberal Party',
        'LIB': 'Manitoba Liberal Party',
        'IND': 'Independent',
    }[abbreviation]


class ManitobaPersonScraper(CanadianScraper):

    def scrape(self):
        member_page = self.lxmlize(COUNCIL_PAGE, encoding='utf-8')
        table = member_page.xpath('//table')[0]
        rows = table.xpath('.//tr')[1:]
        assert len(rows), 'No members found'
        for row in rows:
            (namecell, constitcell, partycell) = row.xpath('.//td')
            full_name = namecell.text_content().strip()
            if full_name.lower() == 'vacant':
                continue
            (last, first) = full_name.split(',')
            name = first.replace('Hon.', '').strip() + ' ' + last.title().strip()
            district = ' '.join(constitcell.text_content().split())
            party = get_party(partycell.text)

            url = namecell.xpath('.//a')[0].get('href')
            photo, email = self.get_details(url)

            p = Person(primary_org='legislature', name=name, district=district, role='MLA',
                       party=party, image=photo)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)
            p.add_contact('email', email)
            yield p

    def get_details(self, url):
        page = self.lxmlize(url)
        photo = page.xpath('//img[@class="page_graphic"]/@src')[0]
        email = self.get_email(page)
        return photo, email

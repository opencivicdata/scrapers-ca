from utils import CanadianScraper, CanadianPerson as Person

import re

COUNCIL_PAGE = 'https://www.northdumfries.ca/en/township-services/mayor-and-council.aspx'


class NorthDumfriesPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        word_to_number = {
            'One': 1,
            'Two': 2,
            'Three': 3,
            'Four': 4,
        }

        councillors = page.xpath('//tr[contains(./td, "Members of Council")]/following-sibling::tr//strong')
        assert len(councillors), 'No councillors found'
        for councillor in councillors:
            match = re.match(r'(?:Ward (\S+) )?(Mayor|Councillor) (.+)', councillor.text_content())
            role = match.group(2)
            name = match.group(3)

            if role == 'Mayor':
                district = 'North Dumfries'
            else:
                district = 'Ward {}'.format(word_to_number[match.group(1)])

            p = Person(primary_org='legislature', name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            node = councillor.xpath('./following-sibling::text()')[0].split('(days)')[0]
            p.add_contact('voice', node, 'legislature')

            node = councillor.xpath('./following-sibling::a/@href')[0]
            if not node.startswith('javascript:'):
                p.add_contact('email', node.replace('mailto:', ''))

            yield p

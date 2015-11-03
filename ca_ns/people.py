from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

import re

COUNCIL_PAGE = 'http://nslegislature.ca/index.php/people/members/'


class NovaScotiaPersonScraper(CanadianScraper):
    PARTIES = {
        'LIB': 'Nova Scotia Liberal Party',
        'PC': 'Progressive Conservative Association of Nova Scotia',
        'NDP': 'Nova Scotia New Democratic Party',
        'IND': 'Independent',
    }

    def scrape(self):
        def char(code):
            try:
                return chr(int(code))
            except ValueError:
                return code

        page = self.lxmlize(COUNCIL_PAGE)
        for row in page.xpath('//div[@id="content"]/table/tbody/tr'):
            if 'Vacant' not in row.xpath('./td//text()')[0]:
                full_name, party, district = row.xpath('./td//text()')[:3]
                name = ' '.join(reversed(full_name.split(',')))

                p = Person(primary_org='legislature', name=name, district=district, role='MLA', party=self.PARTIES[party])

                detail_url = row[0][0].attrib['href']
                detail = self.lxmlize(detail_url)

                image = detail.xpath('//img[@class="portrait"]/@src')[0]
                p.image = image

                try:
                    p.add_contact('voice', detail.xpath('//dd[@class="numbers"]/text()')[0].split(': ')[1], 'legislature')
                except IndexError:
                    pass

                script = detail.xpath('//dd/script/text()')
                if script:
                    codes = reversed(re.findall(r"]='(.+?)'", script[0]))
                    content = ''.join(char(code) for code in codes)
                    p.add_contact('email', re.search(r'>(.+)<', content).group(1))

                p.add_source(COUNCIL_PAGE)
                p.add_source(detail_url)
                yield p

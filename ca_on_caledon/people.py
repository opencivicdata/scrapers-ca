from utils import CanadianScraper, CanadianPerson as Person

import re

COUNCIL_PAGE = 'https://www.caledon.ca/en/townhall/council.asp'


class CaledonPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        node = page.xpath('//td[@rowspan="2"]')[0]
        name = node.xpath('.//h3/strong/text()')[0]
        image = node.xpath('.//@src')[0]
        voice = self.get_phone(node)
        url = node.xpath('.//a[contains(., "Visit")]/@href')[0]

        p = Person(primary_org='legislature', name=name, district='Caledon', role='Mayor')
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)

        p.image = image
        p.add_contact('voice', voice, 'legislature')
        p.add_contact('email', self.get_email(self.lxmlize(url)))

        yield p

        councillors = page.xpath('//div[@id="printAreaContent"]//table[2]//td')
        councillors = councillors[:12] + councillors[16:]
        assert len(councillors), 'No councillors found'
        for i in range(len(councillors) // 3):
            i = i // 4 * 12 + i % 4
            district, role = councillors[i].xpath('.//h3/text()')
            image = councillors[i + 4].xpath('.//@src')[0]
            name = councillors[i + 8].xpath('.//strong/text()')[0]
            voice = self.get_phone(councillors[i + 8])
            url = councillors[i + 8].xpath('.//a[contains(., "Visit")]/@href')[0]

            district = district.replace('\xa0', ' ')
            if ' and ' in district:
                district = district.replace('Ward ', 'Wards ')

            p = Person(primary_org='legislature', name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)

            p.image = image
            p.add_contact('voice', voice, 'legislature')
            p.add_contact('email', self.get_email(self.lxmlize(url)))

            yield p

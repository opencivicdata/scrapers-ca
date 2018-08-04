# coding: utf-8
from utils import CanadianScraper, CanadianPerson as Person

import re

COUNCIL_PAGE = 'https://www.ola.org/en/members/current/contact-information'


class OntarioPersonScraper(CanadianScraper):
    def scrape(self):
        headings = {
            "Queen's Park": 'legislature',
            'Ministry': 'office',
            'Constituency': 'constituency',
        }

        page = self.lxmlize(COUNCIL_PAGE)
        members = page.xpath('//h2[@class="view-grouping-header"]//@href')
        assert len(members), 'No members found'
        for url in members:
            page = self.lxmlize(url)

            name = re.match(r'(.+) \|', page.xpath('//title/text()')[0]).group(1)
            district = page.xpath('//div[contains(@class, "view-display-id-member_riding_block")]//span[@class="field-content"]')[0].text_content()
            party = page.xpath('//div[contains(@class, "view-display-id-current_party_block")]//div[@class="field-content"]/text()')[0]
            image = page.xpath('//div[contains(@class, "view-display-id-member_headshot")]//@src')

            p = Person(primary_org='legislature', name=name, district=district, role='MPP', party=party)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)

            if image:
                p.image = image[0]

            nodes = page.xpath('//div[contains(@class, "views-field-field-email-address")]')
            emails = list(filter(None, [self.get_email(node, error=False) for node in nodes]))
            if emails:
                p.add_contact('email', emails.pop(0))
                if emails:
                    p.extras['constituency_email'] = emails.pop(0)

            for heading, note in headings.items():
                office = page.xpath('//h3[contains(., "{}")]'.format(heading))
                if office:
                    voice = self.get_phone(office[0].xpath('./following-sibling::div[1]')[0], error=False)
                    if voice:
                        p.add_contact('voice', voice, note)

            yield p

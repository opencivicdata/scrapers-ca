from utils import CanadianScraper, CanadianPerson as Person

import re

COUNCIL_PAGE = 'http://www.assembly.gov.nt.ca/meet-members'


class NorthwestTerritoriesPersonScraper(CanadianScraper):
    def scrape(self):
        corrections = {
            'Mackenzie Delta': 'Mackenzie-Delta',
            'Tu Nedhe - Wiilideh': 'Tu Nedhe',
        }

        page = self.lxmlize(COUNCIL_PAGE)

        members = page.xpath('//div[@class="views-field views-field-field-picture"]/parent::td')
        assert len(members), 'No members found'
        for cell in members:
            name = cell[1].text_content().replace(' .', '. ')  # typo on page
            riding = cell[2].text_content().strip()
            riding = corrections.get(riding, riding)

            detail_url = cell[0].xpath('.//a/@href')[0]
            detail_page = self.lxmlize(detail_url)
            photo_url = detail_page.xpath('//div[@class="field-item even"]/img/@src')[0]
            email = self.get_email(detail_page)

            contact_text = ''.join(detail_page.xpath('//div[@property="content:encoded"]/p[1]//text()'))
            phone = re.search(r'P(hone)?: ([-0-9]+)', contact_text)

            p = Person(primary_org='legislature', name=name, district=riding, role='MLA', image=photo_url)
            p.add_source(COUNCIL_PAGE)
            p.add_source(detail_url)
            p.add_contact('email', email)
            if phone:
                p.add_contact('voice', phone.group(2), 'legislature')
            yield p

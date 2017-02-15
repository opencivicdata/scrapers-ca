from utils import CanadianScraper, CanadianPerson as Person

import re

COUNCIL_PAGE = 'http://www.woolwich.ca/en/council/council.asp'


class WoolwichPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//div[@id="printArea"]//strong')
        for councillor in councillors:
            info = councillor.xpath('./parent::p/text()')
            if not info:
                info = councillor.xpath('./parent::div/text()')
            info = [x for x in info if x.strip()]
            district = re.sub('(?<=Ward \d).+', '', info.pop(0))
            if 'Mayor' in district:
                district = 'Woolwich'
                role = 'Mayor'
            else:
                district = district.replace('Councillor', '').strip()
                role = 'Councillor'

            p = Person(primary_org='legislature', name=councillor.text_content(), district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.image = councillor.xpath('./img/@src')[0]

            for contact in info:
                note, num = contact.split(':')
                num = num.strip().replace('(', '').replace(') ', '-').replace('extension ', 'x')
                p.add_contact(note, num, note)
            yield p

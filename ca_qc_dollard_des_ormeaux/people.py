from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

import re

COUNCIL_PAGE = 'http://www.ville.ddo.qc.ca/en/default.asp?contentID=17'


class DollardDesOrmeauxPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, 'iso-8859-1')

        general_contacts = page.xpath('//p[@class="large_title"]/following-sibling::p/text()')
        general_phone = general_contacts[0]
        general_fax = general_contacts[1]

        councillors = page.xpath('//tr/td/p/b')
        for councillor in councillors:
            text = councillor.text_content()
            if '@' in text or 'NEWSLETTER' in text:
                continue

            if 'Mayor' in text:
                name = text.replace('Mayor', '')
                district = 'Dollard-Des Ormeaux'
                role = 'Maire'
            else:
                name = re.split(r'[0-9]', text)[1]
                district = 'District ' + re.findall(r'[0-9]', text)[0]
                role = 'Conseiller'

            p = Person(primary_org='legislature', name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.image = councillor.xpath('./parent::p/parent::td/parent::tr/preceding-sibling::tr//img/@src')[0]

            email = self.get_email(councillor, './parent::p/following-sibling::p')
            p.add_contact('email', email)

            p.add_contact('voice', general_phone, 'legislature')
            p.add_contact('fax', general_fax, 'legislature')

            yield p

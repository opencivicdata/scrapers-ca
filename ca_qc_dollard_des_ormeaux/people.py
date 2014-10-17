from __future__ import unicode_literals
from pupa.scrape import Scraper

import re

from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.ville.ddo.qc.ca/en/default.asp?contentID=17'


class DollardDesOrmeauxPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, 'iso-8859-1')

        general_contacts = page.xpath('//p[@class="large_title"]/following-sibling::p/text()')
        general_phone = general_contacts[0]
        general_fax = general_contacts[1]

        councillors = page.xpath('//tr/td/p/strong')
        councillors = [councillor for councillor in councillors if not "@" in councillor.text_content()]
        for councillor in councillors:

            if 'Mayor' in councillor.text_content():
                name = councillor.text_content().replace('Mayor', '')
                district = 'Dollard-Des Ormeaux'
                role = 'Maire'
            else:
                name = re.split(r'[0-9]', councillor.text_content())[1]
                district = 'District ' + re.findall(r'[0-9]', councillor.text_content())[0]
                role = 'Conseiller'

            p = Person(primary_org='legislature', name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.image = councillor.xpath('./parent::p/parent::td/parent::tr/preceding-sibling::tr//img/@src')[0]

            email = councillor.xpath('./parent::p/following-sibling::p//a[contains(@href, "mailto:")]')
            if email:
                p.add_contact('email', email[0].text_content())

            p.add_contact('voice', general_phone, 'legislature')
            p.add_contact('fax', general_fax, 'legislature')

            yield p

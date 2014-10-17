from __future__ import unicode_literals

import re

from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.ville.kirkland.qc.ca/portrait-municipal/conseil-municipal/elus-municipaux'


class KirklandPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, 'iso-8859-1')

        councillors = page.xpath('//div[@id="PageContent"]/table/tbody/tr/td')
        for councillor in councillors:
            if not councillor.text_content().strip():
                continue
            if councillor == councillors[0]:
                district = 'Kirkland'
                role = 'Maire'
            else:
                district = councillor.xpath('.//h2')[0].text_content()
                district = re.search('- (.+)', district).group(1).strip()
                district = district.replace(' Ouest', ' ouest').replace(' Est', ' est')
                role = 'Conseiller'

            name = councillor.xpath('.//strong/text()')[0]

            phone = councillor.xpath('.//div[contains(text(), "#")]/text()')[0].replace('T ', '').replace(' ', '-').replace(',-#-', ' x')
            email = councillor.xpath('.//a[contains(@href, "mailto:")]')[0].text_content()

            p = Person(primary_org='legislature', name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_contact('voice', phone, 'legislature')
            p.add_contact('email', email)
            p.image = councillor.xpath('.//img/@src')[0]
            yield p

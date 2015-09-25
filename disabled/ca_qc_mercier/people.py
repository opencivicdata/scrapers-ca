from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

import re

COUNCIL_PAGE = 'http://www.ville.mercier.qc.ca/02_viedemocratique/default.asp'


class MercierPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, user_agent='Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)')

        councillors = page.xpath('//table[@width="800"]/tr')
        for councillor in councillors:
            if councillor == councillors[0]:
                name = councillor.xpath('.//strong/text()')[0].replace('Monsieur', '').replace('Madame', '').strip()
                role = 'Maire'
                district = 'Mercier'
            else:
                name = councillor.xpath('.//strong/text()')[0].replace('Monsieur', '').replace('Madame', '').strip()
                role = 'Conseiller'
                district = 'District {}'.format(re.search('(\d)', councillor.xpath('.//text()')[3]).group(1))

            email = self.get_email(councillor)

            p = Person(primary_org='legislature', name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_contact('email', email)
            yield p

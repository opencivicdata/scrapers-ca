# coding: utf-8
from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.vsj.ca/fr/membres-du-conseil.aspx'


class SaintJeromePersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillor_trs = [tr for tr in page.xpath('//table//tr[1]') if len(tr) == 2][:-1]
        for councillor_tr in councillor_trs:
            desc = [text.strip() for text in councillor_tr.xpath('.//text()[normalize-space()]') if text.strip()]
            print(repr(desc))

            if len(desc) == 3:
                role = 'Maire'
                district = 'Saint-Jérôme'
                name = desc[0]
                phone = desc[1]
            else:
                role = 'Conseiller'
                district = desc[0].replace('numéro ', '')
                name = desc[1]
                phone = desc[2]

            email = desc[-1]

            image = councillor_tr.xpath('.//img/@src')[0]

            p = Person(primary_org='legislature', name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.image = image
            p.add_contact('voice', phone, 'legislature')
            p.add_contact('email', email)
            yield p

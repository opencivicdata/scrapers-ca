# coding: utf-8
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.vsj.ca/fr/membres-du-conseil.aspx'


class SaintJeromePersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = [tr for tr in page.xpath('//table//tr[1]') if len(tr) == 2][:-1]
        assert len(councillors), 'No councillors found'
        for i, councillor in enumerate(councillors):
            texts = [text.strip() for text in councillor.xpath('.//text()[normalize-space()]') if text.strip()]

            if 'vacant' in texts[1]:
                continue

            if i == 0:
                role = 'Maire'
                district = 'Saint-Jérôme'
                name = texts[0]
                phone = texts[1]
            else:
                role = 'Conseiller'
                district = texts[0].replace('numéro ', '')
                name = texts[1]
                if len(texts) > 3:
                    phone = texts[2]

            email = texts[-1]

            image = councillor.xpath('.//img/@src')[0]

            p = Person(primary_org='legislature', name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.image = image
            p.add_contact('voice', phone, 'legislature')
            p.add_contact('email', email)
            yield p

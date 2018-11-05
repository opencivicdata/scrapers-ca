from utils import CanadianScraper, CanadianPerson as Person

import re

COUNCIL_PAGE = 'http://www.ville.kirkland.qc.ca/portrait-municipal/conseil-municipal/elus-municipaux'


class KirklandPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, 'iso-8859-1')

        councillors = page.xpath('//div[@id="PageContent"]/table/tbody/tr/td')
        assert len(councillors), 'No councillors found'
        for councillor in councillors:
            if not councillor.text_content().strip():
                continue
            if councillor == councillors[0]:
                district = 'Kirkland'
                role = 'Maire'
            else:
                district = councillor.xpath('.//h2')[0].text_content()
                district = re.search(r'District \d', district).group(0)
                role = 'Conseiller'

            name = councillor.xpath('.//strong/text()')[0]

            phone = councillor.xpath('.//div[contains(text(), "#")]/text()')[0].replace('T ', '').replace(' ', '-').replace(',-#-', ' x')
            email = self.get_email(councillor)

            p = Person(primary_org='legislature', name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_contact('voice', phone, 'legislature')
            p.add_contact('email', email)
            image = councillor.xpath('.//img/@src')
            if image:
                p.image = image[0]
            yield p

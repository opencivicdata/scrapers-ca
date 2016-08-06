from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

import re

COUNCIL_PAGE = 'http://www.ville.brossard.qc.ca/Ma-ville/conseil-municipal.aspx?lang=en-CA'
CONTACT_PAGE = 'http://www.ville.brossard.qc.ca/Ma-ville/conseil-municipal/Municipal-council/Municipal-council-members-%E2%80%93-Contact-information.aspx'


class BrossardPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        contact_page = self.lxmlize(CONTACT_PAGE)

        councillor_elems = page.xpath('//a[contains(@class, "slide item-")]')
        email_links = contact_page.xpath('//a[contains(@href, "mailto:")]')
        for elem in councillor_elems:
            name = elem.xpath('.//div[@class="titre"]/text()')[0]
            if name == 'Poste vacant':
                continue
            if name == 'Francyne Raymond':
                name = 'Francine Raymond'  # her name is Francine on the contact page, not Francyne
            position = elem.xpath('.//div[@class="poste"]/text()')[0]
            role = 'Conseiller'
            district = re.search(r'District \d+', position)
            if district:
                district = district.group(0)
            elif 'Mayor' in position:
                district = 'Brossard'
                role = 'Maire'

            photo = re.search(r'url\((.+)\)', elem.attrib['style']).group(1)

            p = Person(primary_org='legislature', name=name, district=district, role=role, image=photo)
            p.add_source(COUNCIL_PAGE)
            p.add_source(CONTACT_PAGE)

            email_elem = [link for link in email_links
                          if name in link.text_content().replace('\u2019', "'")][0]
            email = re.match('mailto:(.+@brossard.ca)', email_elem.attrib['href']).group(1)
            p.add_contact('email', email)
            phone = email_elem.xpath('./following-sibling::text()[contains(., "450")]')[0]
            p.add_contact('voice', phone, 'legislature')

            yield p

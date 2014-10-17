# coding: utf-8
from __future__ import unicode_literals
from pupa.scrape import Scraper

import re

from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.ville.brossard.qc.ca/Ma-ville/conseil-municipal.aspx?lang=en-CA'


class BrossardPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillor_elems = page.xpath('//a[contains(@class, "slide item-")]')
        email_links = page.xpath('//a[contains(@href, "mailto:")]')
        for elem in councillor_elems:
            name_elem = elem.xpath('.//strong')[0]
            name = re.search('(Mr\. )?(.+)', name_elem.text).group(2)
            position = name_elem.xpath('string(following-sibling::text())')
            role = 'Conseiller'
            if 'Mayor' in position:
                district = 'Brossard'
                role = 'Maire'
            else:
                district = re.sub(r'(?<=[0-9]).+', '', position).strip()

            photo = re.search(r'url\((.+)\)', elem.attrib['style']).group(1)

            p = Person(primary_org='legislature', name=name, district=district, role=role, image=photo)
            p.add_source(COUNCIL_PAGE)

            try:
                email_elem = [link for link in email_links
                              if name in link.text_content().replace('\u2019', "'")][0]
                email = re.match('mailto:(.+@brossard.ca)', email_elem.attrib['href']).group(1)
                p.add_contact('email', email)
                phone = email_elem.xpath(
                    './following-sibling::text()[contains(., "450")]')[0]
                p.add_contact('voice', phone, 'legislature')
            except IndexError:  # oh Francyne/Francine Raymond, who are you, really?
                pass

            yield p

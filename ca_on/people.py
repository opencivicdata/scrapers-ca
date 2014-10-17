# coding: utf-8
from __future__ import unicode_literals
from pupa.scrape import Scraper

import re

from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.ontla.on.ca/web/members/member_addresses.do'


class OntarioPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        for block in page.xpath('//div[@class="addressblock"]'):
            name_elem = block.xpath('.//a[@class="mpp"]')[0]
            name = ' '.join(name_elem.text.split())
            riding = block.xpath(
                'string(.//div[@class="riding"])').replace('--', '\u2014').replace('Chatham—Kent', 'Chatham-Kent')  # m-dash to hyphen
            email = block.xpath('string(.//a[contains(@href, "mailto:")])')
            phone = block.xpath('string(.//div[@class="phone"])')
            mpp_url = name_elem.attrib['href']
            mpp_page = self.lxmlize(mpp_url)
            photo_url = mpp_page.xpath('string(//img[@class="mppimg"]/@src)')
            party = mpp_page.xpath('string(//div[@class="partyaffil"]/h3)')
            p = Person(primary_org='legislature', name=name, district=riding, role='MPP',
                       party=party, image=photo_url)
            p.add_source(COUNCIL_PAGE)
            p.add_source(mpp_url)
            if email:
                p.add_contact('email', email)
            elif name == 'Arthur Potts':
                p.add_contact('email', 'apotts.mpp.co@liberal.ola.org')
            p.add_contact('voice', phone, 'legislature')
            yield p

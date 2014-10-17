from __future__ import unicode_literals
from pupa.scrape import Scraper

import re

from six.moves import html_parser

from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.beaconsfield.ca/en/your-council.html'


class BeaconsfieldPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//h1[@class="title"]')
        for councillor in councillors:
            if ',' not in councillor.text_content():
                continue
            name, district = councillor.text_content().split(',')
            name = name.strip()
            if 'Mayor' in district:
                p = Person(primary_org='legislature', name=name, district='Beaconsfield', role='Maire')
                p.add_source(COUNCIL_PAGE)
                p.image = councillor.xpath('./parent::div/parent::div/p//img/@src')[0]
                phone = councillor.xpath('.//parent::div/following-sibling::div[contains(text(), "514")]/text()')[0]
                phone = phone.split(':')[1].strip().replace(' ', '-')
                p.add_contact('voice', phone, 'legislature')
                script = councillor.xpath('.//parent::div/following-sibling::div/script')[0].text_content()
                p.add_contact('email', get_email(script))
                yield p
                continue

            district = district.split('-')[1].strip()
            p = Person(primary_org='legislature', name=name, district=district, role='Conseiller')
            p.add_source(COUNCIL_PAGE)

            p.image = councillor.xpath('./parent::div/parent::div/p//img/@src')[0]

            phone = councillor.xpath('.//parent::div/following-sibling::p[contains(text(), "514")]/text()')
            if phone:
                phone = phone[0]
                phone = phone.split(':')[1].strip().replace(' ', '-')
                p.add_contact('voice', phone, 'legislature')
            script = councillor.xpath('.//parent::div/following-sibling::p/script')[0].text_content()
            p.add_contact('email', get_email(script))
            yield p


def get_email(script):
    var = re.findall(r'var addy\d{4,5} = \'(.*)\'', script)[0].replace('\' + \'', '').replace('\'', '')
    ext = re.findall(r'addy\d{4,5} = addy\d{4,5} \+ \'(.*);', script)[0].replace('\' + \'', '').replace('\'', '')
    h = html_parser.HTMLParser()
    email = h.unescape(var + ext)
    return email

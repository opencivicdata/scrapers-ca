from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

import re
from collections import defaultdict
from itertools import takewhile

from six.moves.urllib.parse import urljoin

COUNCIL_PAGE = 'http://www.regionofwaterloo.ca/en/regionalgovernment/regionalcouncil.asp'
CHAIR_URL = 'http://www.regionofwaterloo.ca/en/regionalGovernment/regionalchairandsupportstaff.asp'


class WaterlooPersonScraper(CanadianScraper):

    def scrape(self):
        seat_numbers = defaultdict(int)

        page = self.lxmlize(COUNCIL_PAGE)

        regions = page.xpath('//*[@id="contentIntleft"]//h3')[2:]
        for region in regions:
            # the links in all <p> tags immediately following each <h3>
            councillors = [elem[0] for elem in
                           takewhile(lambda elem: elem.tag == 'p',
                                     region.xpath('./following-sibling::*'))]
            for i, councillor in enumerate(councillors):
                post = re.search('of (.*)', region.text).group(1)
                if i == 0:
                    district = post
                else:
                    seat_numbers[post] += 1
                    district = '%s (seat %d)' % (post, seat_numbers[post])
                p = Person(primary_org='legislature', name=councillor.text, district=district, role='Regional Councillor')
                p.add_source(COUNCIL_PAGE)
                councillor_url = councillor.attrib['href']
                p.add_source(councillor_url)
                email, phone, photo_url = self.councillor_data(councillor_url)
                if email:
                    p.add_contact('email', email)
                if phone:
                    p.add_contact('voice', phone, 'legislature')
                if photo_url:
                    p.image = photo_url
                yield p

        chairpage = self.lxmlize(CHAIR_URL)
        name = chairpage.xpath('//h1')[0].text_content().replace('Meet ', '')
        param = chairpage.xpath('//div[@class="contactBodyContactInfoContactModuleV2"]/@id')[0].replace('contactEntry_', '')
        contact = self.lxmlize('http://www.regionofwaterloo.ca/en/ContactModule/services/GetContactHTML.ashx?param=%s' % param)
        email = self.get_email(contact, error=False)
        phone = self.get_phone(contact, area_codes=[226, 519])
        photo_url_src = chairpage.xpath('//div[@id="contentIntleft"]//img[1]/@src')[0]
        photo_url = urljoin(CHAIR_URL, photo_url_src)
        p = Person(primary_org='legislature', name=name, district='Waterloo', role='Chair')
        p.add_source(CHAIR_URL)
        if email:
            p.add_contact('email', email)
        p.add_contact('voice', phone, 'legislature')
        p.image = photo_url
        yield p

    def councillor_data(self, url):
        page = self.lxmlize(url)
        contact = page.xpath('//div[@class="contactBodyContactInfoContactModuleV2"]')
        email = None
        phone = None
        photo_url = None
        if contact:
            contact = contact[0]
            if not contact.text_content().strip():
                param = contact.xpath('./@id')[0].replace('contactEntry_', '')
                contact = self.lxmlize('http://www.regionofwaterloo.ca/en/ContactModule/services/GetContactHTML.ashx?param=%s' % param)
            email = self.get_email(contact, error=False)
            phone = self.get_phone(contact, area_codes=[226, 519])

        photo_elem = page.xpath('//div[@id="contentIntleft"]//img[1]/@src')
        if photo_elem:
            photo_url_src = photo_elem[0]
            photo_url = urljoin(url, photo_url_src)
        return email, phone, photo_url

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

        regions = page.xpath('//*[@id="contentIntleft"]//h3')[1:]
        for region in regions:
            # the links in all <p> tags immediately following each <h3>
            councillors = [elem[0] for elem in
                           takewhile(lambda elem: elem.tag == 'p',
                                     region.xpath('./following-sibling::*'))]
            for councillor in councillors:
                post = re.search('of (.*)', region.text).group(1)
                if 'Mayor' in councillor.xpath('../text()')[0]:
                    district = '%s (mayor)' % post
                else:
                    seat_numbers[post] += 1
                    district = '%s (seat %d)' % (post, seat_numbers[post])
                p = Person(primary_org='legislature', name=councillor.text, district=district, role='Councillor')
                p.add_source(COUNCIL_PAGE)
                councillor_url = councillor.attrib['href']
                p.add_source(councillor_url)
                email, phone, address, photo_url = self.councillor_data(councillor_url)
                p.add_contact('email', email)
                p.add_contact('voice', phone, 'legislature')
                p.add_contact('address', address, 'legislature')
                p.image = photo_url
                yield p

        chairpage = self.lxmlize(CHAIR_URL)
        name = re.search('Chair (.*) -',
                         chairpage.xpath('string(//title)')).group(1)
        email = chairpage.xpath('string(//a[contains(text(), "E-mail")]/@href)')
        phone = chairpage.xpath('string((//span[@class="labelTag"][contains(text(), "Phone")]/parent::*/text())[1])').strip(':')
        address = '\n'.join(
            chairpage.xpath('//div[@class="contactBody"]//p[1]/text()'))
        photo_url_src = chairpage.xpath(
            'string(//div[@id="contentIntleft"]//img[1]/@src)')
        photo_url = urljoin(CHAIR_URL, photo_url_src)
        p = Person(primary_org='legislature', name=name, district='Waterloo', role='Chair')
        p.add_source(CHAIR_URL)
        p.add_contact('email', email)
        p.add_contact('voice', phone, 'legislature')
        p.add_contact('address', address, 'legislature')
        p.image = photo_url
        yield p

    def councillor_data(self, url):
        page = self.lxmlize(url)
        email = page.xpath('string(//a[contains(text(), "Email Councillor")]/@href)')
        phone = page.xpath('string((//span[@class="labelTag"][contains(text(), "Phone")]/parent::*/text())[1])').strip(':')
        address = '\n'.join(page.xpath('//div[@class="contactBody"]//p[1]/text()'))
        photo_url_src = page.xpath('string(//div[@id="contentIntleft"]//img[1]/@src)')
        photo_url = urljoin(url, photo_url_src)
        return email, phone, address, photo_url

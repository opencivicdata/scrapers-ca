# coding: utf-8
from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.ontla.on.ca/web/members/member_addresses.do'


class OntarioPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        for block in page.xpath('//div[@class="addressblock"]'):
            name_elem = block.xpath('.//a[@class="mpp"]')[0]
            name = ' '.join(name_elem.text.split())

            if 'Joe Cimino' not in name:  # no more MPP
                riding = block.xpath('.//div[@class="riding"]//text()')[0].strip()
                district = riding.replace('--', '\u2014').replace('Chatham—Kent', 'Chatham-Kent')  # m-dash to hyphen
                email = self.get_email(block.xpath('.//div[@class="email"]')[0])
                phone = block.xpath('.//div[@class="phone"]//text()')[0]
                mpp_url = name_elem.attrib['href']

                mpp_page = self.lxmlize(mpp_url)

                if riding in mpp_page.xpath('//h1/text()')[0]:
                    photo_url = mpp_page.xpath('//img[@class="mppimg"]/@src')[0]
                    party = mpp_page.xpath('//div[@class="mppinfoblock"]/p[last()]/text()')[0].strip()

                    p = Person(primary_org='legislature', name=name, district=district, role='MPP',
                               party=party, image=photo_url)
                    p.add_source(COUNCIL_PAGE)
                    p.add_source(mpp_url)
                    if email:
                        p.add_contact('email', email)
                    p.add_contact('voice', phone, 'legislature')
                    yield p
                else:
                    self.warning('MPP addresses out of sync with current MPPs (%s)' % riding)

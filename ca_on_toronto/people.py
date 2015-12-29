from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

import re

COUNCIL_PAGE = 'http://www1.toronto.ca/wps/portal/contentonly?vgnextoid=c3a83293dc3ef310VgnVCM10000071d60f89RCRD'

OTHER_NAMES = {
    'Norm Kelly': ['Norman Kelly'],
    'Justin Di Ciano': ['Justin J. Di Ciano'],
    }

class TorontoPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        a = page.xpath('//a[contains(text(),"Mayor")]')[0]
        yield self.scrape_mayor(a.attrib['href'])

        for a in page.xpath('//table')[0].xpath('.//a[contains(text(),"Councillor")]'):
            page = self.lxmlize(a.attrib['href'])
            h1 = page.xpath('//h1//text()')[0]
            if 'Council seat is vacant' not in h1:
                yield self.scrape_councilor(page, h1, a.attrib['href'])

    def scrape_councilor(self, page, h1, url):
        name = h1.split('Councillor')[1].strip()
        ward_full = page.xpath('//p/descendant-or-self::*[contains(text(), "Profile:")]/text()')[0].replace('\xa0', ' ')
        ward_num, ward_name = re.search(r'Ward (\d+) (.+)', ward_full).groups()
        if ward_name == 'Etobicoke Lakeshore':
            ward_name = 'Etobicoke-Lakeshore'

        ward_name = ward_name.replace('-', '\u2014')

        district = '{0} ({1})'.format(ward_name, ward_num)

        p = Person(primary_org='legislature', name=name, district=district, role='Councillor')
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)
        p.extras = {
            'ward_number': ward_num,
            'ward_name': ward_name,
            }

        for name in OTHER_NAMES.get(name, []):
            p.add_name(name)

        p.image = page.xpath('//main//img/@src')[0].replace('www.', 'www1.')  # @todo fix lxmlize to use the redirected URL to make links absolute
        email = self.get_email(page)
        p.add_contact('email', email)

        addr_cell = page.xpath('//*[contains(text(), "Toronto City Hall")]/ancestor::td')[0]
        phone = (addr_cell.xpath('(.//text()[contains(., "Phone:")])[1]')[0]
                          .split(':')[1])
        p.add_contact('voice', phone, 'legislature')

        address = '\n'.join(addr_cell.xpath('./p[2]/text()')[:2])
        if address:
            p.add_contact('address', address, 'legislature')

        return p

    def scrape_mayor(self, url):
        page = self.lxmlize(url)
        name = page.xpath('//meta[@property="og:description"]/@content')[0].replace('Office of the Mayor of Toronto, ', '').strip()

        p = Person(primary_org='legislature', name=name, district="Toronto", role='Mayor')
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)

        p.image = page.xpath('//article/img/@src')[0].replace('www.', 'www1.')

        url = page.xpath('//a[contains(text(), "Contact the Mayor")]')[0].attrib['href'].replace('www.', 'www1.')
        p.add_source(url)
        page = self.lxmlize(url)

        mail_elem, email_elem, phone_elem = page.xpath('//article[contains(@class,"col-sm-6")]//header')[:3]
        address = ''.join(mail_elem.xpath('./following-sibling::p//text()'))
        phone = phone_elem.xpath('./following-sibling::p[1]//text()')[0]
        email = email_elem.xpath('./following-sibling::p[1]//text()')[0]

        p.add_contact('address', address, 'legislature')
        p.add_contact('voice', phone, 'legislature')
        p.add_contact('email', email)
        return p

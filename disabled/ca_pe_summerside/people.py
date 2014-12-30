from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person, CONTACT_DETAIL_TYPE_MAP

import re

from six.moves.urllib.parse import urljoin

COUNCIL_PAGE = 'http://city.summerside.pe.ca/mayor-and-council/pages/2012/2/councillors/'
MAYOR_PAGE = 'http://city.summerside.pe.ca/mayor-and-council/pages/2012/2/mayor/'


class SummersidePersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, 'iso-8859-1')

        yield self.scrape_mayor()

        councillors = page.xpath('//div[@class="articlebody-inside"]//p[contains(text(),"-")]')
        for councillor in councillors:
            url = councillor.xpath('.//a')[0].attrib['href'].replace('../', '')
            page = self.lxmlize(url, 'iso-8859-1')

            name = page.xpath('//div[@class="articletitle"]/h1')[0].text_content().replace('Councillor', '').replace('Deputy Mayor', '')
            district = 'Ward %s' % re.sub('\D+', '', page.xpath('//div[@class="articlebody-inside"]/p')[0].text_content())

            p = Person(primary_org='legislature', name=name, district=district, role='Councillor')
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)

            photo_url_rel = page.xpath('//div[@class="articlebody-inside"]/p/img/@src')[0].replace('/..', '')
            p.image = urljoin(url, photo_url_rel)

            contacts = page.xpath('//div[@class="articlebody-inside"]/p')[1].text_content().replace('Biography', '').replace('Committees', '').split(':')
            for i, contact in enumerate(contacts):
                if i == 0 or not contact:
                    continue
                contact_type = re.findall(r'([A-Z][a-z]+)', contacts[i - 1])[0]
                if contact_type != 'Address':
                    contact = re.split(r'[A-Z]', contact)[0]
                contact_type = CONTACT_DETAIL_TYPE_MAP[contact_type]
                p.add_contact(contact_type, contact, '' if contact_type == 'email' else 'legislature')
            yield p

    def scrape_mayor(self):
        page = self.lxmlize(MAYOR_PAGE, 'iso-8859-1')

        name = page.xpath('//div[@class="articletitle"]/h1')[0].text_content().replace('Mayor', '')

        p = Person(primary_org='legislature', name=name, district='Summerside', role='Mayor')
        p.add_source(MAYOR_PAGE)
        p.image = page.xpath('//div[@class="articlebody-inside"]/p/img/@src')[0].replace('..', '')

        info = page.xpath('//div[@class="articlebody-inside"]/p')
        phone = re.findall(r'to (.*)', info[1].text_content())[0]
        address = info[3].text_content().replace('by mail: ', '') + ' ' + info[4].text_content()
        email = self.get_email(info[5])

        p.add_contact('voice', phone, 'legislature')
        p.add_contact('address', address, 'legislature')
        p.add_contact('email', email)

        return p

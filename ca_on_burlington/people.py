from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

import re

COUNCIL_PAGE = 'http://cms.burlington.ca/Page110.aspx'


class BurlingtonPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//div[@id="subnav"]//a')
        for councillor in councillors:
            name = councillor.xpath('./span/text()')[0].strip()
            district = councillor.xpath('.//strong')[0].text_content()

            url = councillor.attrib['href']

            if councillor == councillors[0]:
                yield self.scrape_mayor(name, url)
                continue

            page = self.lxmlize(url)

            address = page.xpath('//div[@id="content"]//p[contains(text(),"City of Burlington,")]')
            contact = page.xpath('//div[@id="subnav"]//p[contains(text(),"Phone")]')[0]
            phone = re.findall(r'Phone: (.*)', contact.text_content())[0].replace('Ext. ', 'x').replace('#', 'x')
            fax = re.findall(r'Fax: (.*)', contact.text_content())[0]
            email = self.get_email(contact)

            p = Person(primary_org='legislature', name=name, district=district, role='Councillor')
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)

            p.image = page.xpath('//div[@id="subnav"]//img/@src')[0]

            if address:
                p.add_contact('address', address[0].text_content(), 'legislature')
            p.add_contact('voice', phone, 'legislature')
            p.add_contact('fax', fax, 'legislature')
            p.add_contact('email', email)

            yield p

    def scrape_mayor(self, name, url):
        page = self.lxmlize(url)

        contact = page.xpath('//div[@id="secondary align_RightSideBar"]/blockquote/p/text()')
        phone = contact[0]
        fax = contact[1]
        email = self.get_email(page, '//div[@id="secondary align_RightSideBar"]/blockquote/p')

        mayor_page = self.lxmlize('http://www.burlingtonmayor.com')
        contact_url = mayor_page.xpath('//div[@class="menu"]//a[contains(text(),"Contact")]')[0].attrib['href']
        mayor_page = self.lxmlize(contact_url)
        address = mayor_page.xpath('//div[@class="entry-content"]//p[contains(text(),"City Hall")]')[0].text_content()

        p = Person(primary_org='legislature', name=name, district="Burlington", role='Mayor')
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)
        p.add_source('http://www.burlingtonmayor.com')

        p.image = page.xpath('//div[@id="secondary align_RightSideBar"]/p/img/@src')[0]
        p.add_contact('voice', phone, 'legislature')
        p.add_contact('fax', fax, 'legislature')
        p.add_contact('email', email)
        p.add_contact('address', address, 'legislature')

        return p

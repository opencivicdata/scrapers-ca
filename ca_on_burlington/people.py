from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person


COUNCIL_PAGE = 'http://www.burlington.ca/en/services-for-you/Council-Members-and-Wards.asp?_mid_=754'


class BurlingtonPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//div[@id="landingNav"]//a')
        for councillor in councillors:
            district = councillor.xpath('./text()')[0]

            if district == 'Mayor':
                role = 'Mayor'
                district = 'Burlington'
            else:
                role = 'Councillor'

            url = councillor.attrib['href']
            councillor_page = self.lxmlize(url)

            name = councillor_page.xpath('//h1/text()')[0].split(' ', 1)[1]
            address = ' '.join(councillor_page.xpath('//div[@id="printAreaContent"]//p[contains(text(),"City of Burlington")]/text()'))

            contact_info = councillor_page.xpath('//h2[contains(text(), "Contacts")]/following-sibling::p[1]//text()')
            phone = contact_info[1].split('Tel:')[1].replace('Ext. ', 'x').replace('#', 'x')
            fax = contact_info[2].split('Fax:')[1]
            email = contact_info[-1]

            # Pictures are embedded in a banner
            p = Person(primary_org='legislature', name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)
            p.add_contact('address', address, 'legislature')
            p.add_contact('voice', phone, 'legislature')
            p.add_contact('fax', fax, 'legislature')
            p.add_contact('email', email)

            yield p

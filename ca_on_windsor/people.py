from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.citywindsor.ca/mayorandcouncil/City-Councillors/Pages/City-Councillors.aspx'
MAYOR_COUNCIL_PAGE = 'http://www.citywindsor.ca/mayorandcouncil/Pages/Mayor-and-City-Council.aspx'


class WindsorPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//h2/ancestor::div[1]')
        for councillor in councillors:
            district, name = councillor.xpath('./h2//text()')[0].split(' – ')
            p = Person(primary_org='legislature', name=name, district=district, role='Councillor')
            p.add_source(COUNCIL_PAGE)

            email = self.get_email(councillor)
            p.add_contact('email', email)

            phone = self.get_phone(councillor, [519])
            p.add_contact('voice', phone, 'legislature')

            p.image = councillor.xpath('./h2//img/@src')[0]

            yield p

        page = self.lxmlize(MAYOR_COUNCIL_PAGE)
        contact_details = page.xpath('//p[contains(.//text(), "Mayor\'s Office")]')[0]
        address = ' '.join(contact_details.xpath('text()')[:5])
        phone, fax = contact_details.xpath('text()')[5:7]
        phone = phone.strip().replace('(', '').replace(') ', '-')
        fax = fax.strip().replace('(', '').replace(') ', '-').split(':')[1]
        email = self.get_email(contact_details)
        image = page.xpath('//p[@class="sectioning"]/a[contains(@title, "Mayor")]/img/@src')[0]

        mayor_url = page.xpath('//a[contains(@title, "Mayor")]/@href')[0]
        mayor_page = self.lxmlize(mayor_url)
        name = mayor_page.xpath('//div[@id="CCWMainContent2"]//h1//text()')[0].split(' ', 1)[1]

        p = Person(primary_org='legislature', name=name, district='Windsor', role='Mayor')
        p.add_source(MAYOR_COUNCIL_PAGE)
        p.add_source(mayor_url)
        p.add_contact('address', address, 'legislature')
        p.add_contact('voice', phone, 'legislature')
        p.add_contact('fax', fax, 'legislature')
        p.add_contact('email', email)
        p.image = image
        yield p

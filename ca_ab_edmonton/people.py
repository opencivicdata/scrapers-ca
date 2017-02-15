from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.edmonton.ca/city_government/city_organization/city-councillors.aspx'
MAYOR_PAGE = 'http://www.edmonton.ca/city_government/city_organization/the-mayor.aspx'


class EdmontonPersonScraper(CanadianScraper):
    def scrape(self):
        yield self.scrape_mayor()
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//div[contains(@class, "documentexcerpt-module__item")]')
        assert len(councillors), 'No councillors found'
        for cell in councillors:
            name = cell[1].text
            if name != 'Vacant':
                page_url = cell[0].attrib['href']
                page = self.lxmlize(page_url)
                district_name = page.xpath('//h1[contains(@class, "page-title")]')[0].text_content()
                district, name = district_name.split(' - ', 1)

                p = Person(primary_org='legislature', name=name, district=district, role='Councillor')
                p.add_source(COUNCIL_PAGE)
                p.add_source(page_url)

                image = page.xpath('//div[contains(@class, "content")]//img/@src')
                if image:
                    p.image = image[0]

                address = page.xpath('//address//p')
                if address:
                    address = address[0].text_content()
                    p.add_contact('address', address, 'legislature')

                contacts = page.xpath('//table[@summary="Contact information"]//tr')
                for contact in contacts:
                    contact_type = contact.xpath('./th/text()')[0]
                    value = contact.xpath('./td//text()')[0]
                    if 'Title' in contact_type:
                        continue
                    elif 'Website' in contact_type or 'Facebook' in contact_type or 'Twitter' in contact_type:
                        value = contact.xpath('./td/a/text()')[0]
                        p.add_link(value)
                    elif 'Telephone' in contact_type:
                        p.add_contact('voice', value, 'legislature')
                    elif 'Fax' in contact_type:
                        p.add_contact('fax', value, 'legislature')
                    elif 'Email' in contact_type:
                        p.add_contact('email', value)
                yield p

    def scrape_mayor(self):
        page = self.lxmlize(MAYOR_PAGE)
        name = page.xpath('//h1[contains(text(), "Mayor")]/text()')[0].replace('Mayor', '').strip()

        p = Person(primary_org='legislature', name=name, district='Edmonton', role='Mayor')
        p.add_source(MAYOR_PAGE)

        address = ' '.join(page.xpath('//address/p/text()'))
        p.add_contact('address', address, 'legislature')

        return p

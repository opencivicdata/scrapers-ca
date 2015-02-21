from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = "https://www.saskatoon.ca/city-hall/mayor-city-councillors/city-councillors"
MAYOR_PAGE = "https://www.saskatoon.ca/city-hall/mayor-city-councillors/mayors-office"
EMAIL_URL = "https://www.saskatoon.ca/city-hall/mayor-city-councillors/contact-your-city-councillor"


class SaskatoonPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        yield self.scrape_mayor()

        email_page = self.lxmlize(EMAIL_URL)
        c_options = email_page.xpath('//select[@id="edit-submitted-councillor"]/option[contains(text(), "Ward")]')
        email_dict = dict((opt.text.split(' - ')[0], opt.attrib['value']) for
                          opt in c_options)

        councillors = page.xpath('//h2[@class="landing-block-title"]/a')[:-1]
        for councillor in councillors:
            url = councillor.attrib['href']
            page = self.lxmlize(url)

            district = page.xpath('//div[@id="main-content"]/h1/text()')[0]
            name = page.xpath('//div[@id="main-content"]/h2/text()')[0]

            p = Person(primary_org='legislature', name=name, district=district, role='Councillor')
            p.add_source(COUNCIL_PAGE)
            p.add_source(EMAIL_URL)
            p.add_source(url)

            if district in email_dict:
                p.add_contact('email', email_dict[district])

            contacts = page.xpath('//aside[@class="page-sidebar"]/div[1]/p')
            for contact in contacts[:-1]:
                contact_type = contact.xpath('./strong/text()')[0]
                if 'Contact' in contact_type:
                    continue
                value = contact.xpath('./a/text()')[0]
                if 'Fax' in contact_type:
                    p.add_contact('fax', value, 'legislature')
                if 'Phone' in contact_type:
                    p.add_contact(contact_type, value, contact_type)

            yield p

    def scrape_mayor(self):
        page = self.lxmlize(MAYOR_PAGE)
        image = page.xpath('//img[contains(@alt, "Mayor")]/@src')[0]

        contact_url = page.xpath('//a[contains(text(), "Contact the Mayor")]/@href')[0]
        contact_page = self.lxmlize(contact_url)

        infos = contact_page.xpath('//h4[contains(text(), "Address")]/following-sibling::p')
        name = ' '.join(infos[0].text_content().split('\n')[0].split()[2:])
        address = ' '.join(infos[0].text_content().split('\n')[1:])
        phone = infos[1].text_content().split('\n')[0].replace('Phone', '')
        fax = infos[1].text_content().split('\n')[1].replace('Fax', '')

        p = Person(primary_org='legislature', name=name, district='Saskatoon', role='Mayor')
        p.add_source(MAYOR_PAGE)
        p.add_source(contact_url)
        p.image = image
        p.add_contact('address', address, 'legislature')
        p.add_contact('voice', phone, 'legislature')
        p.add_contact('fax', fax, 'legislature')
        return p

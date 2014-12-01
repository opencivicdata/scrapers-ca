from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

import re

COUNCIL_PAGE = "http://www.saskatoon.ca/CITY%20COUNCIL/YOUR%20WARD%20COUNCILLORS/Pages/default.aspx"
EMAIL_URL = "http://apps2.saskatoon.ca/app/aForms/councillor.aspx"


class SaskatoonPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        mayor_url = page.xpath('//td[@class="sask_LeftNavLinkContainer"]/a/@href')[0]
        yield self.scrape_mayor(mayor_url)

        email_page = self.lxmlize(EMAIL_URL)
        c_options = email_page.xpath(
            '//select[@id="councillorList"]/option[contains(text(), "Ward")]')
        email_dict = dict((opt.text.split(' - ')[0], opt.attrib['value']) for
                          opt in c_options)

        councillors = page.xpath('//td[@class="sask_LeftNavChildNodeContainer"]//a')
        for councillor in councillors:
            district, name = councillor.text_content().split(' - Councillor ')
            url = councillor.attrib['href']

            p = Person(primary_org='legislature', name=name, district=district, role='Councillor')
            p.add_source(COUNCIL_PAGE)
            p.add_source(EMAIL_URL)
            p.add_source(url)

            page = self.lxmlize(url)
            try:
                p.add_contact('email', email_dict[district])
            except KeyError:
                email = page.xpath('//a[contains(@href, "mailto:")]/@href')[0]
                p.add_contact('email', email)

            contacts = page.xpath('//p[@class="para12"]')[0]
            if not contacts.text_content().strip():
                contacts = page.xpath('//p[@class="para12"]')[1]
            contacts = re.split(r'\xa0', contacts.text_content())
            contacts = [x for x in contacts if x.strip()]
            for i, contact in enumerate(contacts):
                if 'Contact' in contact:
                    continue
                if contact == contacts[-1]:
                    break
                contact_type = contact.replace(':', '').strip()
                value = contacts[i + 1].replace('(', '').replace(') ', '-').strip()
                if 'Fax' in contact_type:
                    p.add_contact('fax', value, 'legislature')
                if 'Phone' in contact_type:
                    p.add_contact(contact_type, value, contact_type)
            yield p

    def scrape_mayor(self, url):
        page = self.lxmlize(url)
        name = page.xpath('//tr/td/p')[-1]
        name = name.text_content().replace('Mayor', '')
        image = page.xpath('//div[@class="sask_ArticleBody"]//img/@src')[0]

        contact_url = page.xpath('//a[contains(text(), "Contact the Mayor")]/@href')[0]
        page = self.lxmlize(contact_url)

        address = ' '.join(page.xpath('//div[@id="ctl00_PlaceHolderMain_RichHtmlField1__ControlWrapper_RichHtmlField"]/p[4]/text()')[1:])
        phone = page.xpath('//div[@id="ctl00_PlaceHolderMain_RichHtmlField1__ControlWrapper_RichHtmlField"]/p[5]/span/text()')[0].replace('(', '').replace(') ', '-')
        fax = page.xpath('//div[@id="ctl00_PlaceHolderMain_RichHtmlField1__ControlWrapper_RichHtmlField"]/p[6]/span/text()')[0].replace('(', '').replace(') ', '-')

        p = Person(primary_org='legislature', name=name, district='Saskatoon', role='Mayor')
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)
        p.image = image
        p.add_contact('address', address, 'legislature')
        p.add_contact('voice', phone, 'legislature')
        p.add_contact('fax', fax, 'legislature')
        return p

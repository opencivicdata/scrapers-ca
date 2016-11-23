from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

import re

COUNCIL_PAGE = 'http://www.vaughan.ca/council/Pages/default.aspx'


class VaughanPersonScraper(CanadianScraper):

    def scrape(self):
        regional_councillor_seat_number = 1

        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//div[@id="WebPartWPQ3"]//ul[@class="dfwp-list"][1]/li/div/div/a')
        assert len(councillors), 'No councillors found'
        for councillor in councillors:
            url = councillor.attrib['href']
            page = self.lxmlize(url)

            title = page.xpath('//div[@class="PL_Title"]')[0].text_content()
            if "Councillor" in title:
                district, name = re.split(r'Councillor', title)
                role = 'Councillor'
                if "Regional" in district:
                    role = 'Regional Councillor'
                    district = "Vaughan (seat {})".format(regional_councillor_seat_number)
                    regional_councillor_seat_number += 1
            else:
                name = re.search(r'Mayor ([^,]+)', page.xpath('//meta[@name="keywords"]/@content')[0]).group(1)
                district = 'Vaughan'
                role = 'Mayor'
            name = name.strip()

            if role == 'Mayor':
                detail = self.lxmlize(page.xpath('//a[contains(@href,"/Contact-the-Mayor")]/@href')[0])
                contact_info = detail.xpath('//div[@id="ctl00_PlaceHolderMain_RichHtmlField1__ControlWrapper_RichHtmlField"]')[0]
            else:
                contact_node = page.xpath('//div[contains(@id, "WebPartWPQ")][contains(., "Phone")]')
                if contact_node:
                    contact_info = contact_node[0]
                else:
                    contact_info = page.xpath('//div[@id="WebPartWPQ3"]')[0]

            phone = re.findall(r'[0-9]{3}-[0-9]{3}-[0-9]{4} ext\. [0-9]{4}', contact_info.text_content())[0].replace('ext. ', 'x')
            fax = re.findall(r'[0-9]{3}-[0-9]{3}-[0-9]{4}', contact_info.text_content())[1]
            email = self.get_email(contact_info)

            p = Person(primary_org='legislature', name=name, district=district.strip(), role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)
            p.add_contact('voice', phone, 'legislature')
            p.add_contact('fax', fax, 'legislature')
            p.add_contact('email', email)

            image = page.xpath('//img[contains(@alt, "Councillor")]/@src')
            if image:
                p.image = image[0]

            if page.xpath('.//a[contains(@href,"facebook")]'):
                p.add_link(page.xpath('.//a[contains(@href,"facebook")]')[0].attrib['href'])
            if page.xpath('.//a[contains(@href,"twitter")]'):
                p.add_link(page.xpath('.//a[contains(@href,"twitter")]')[0].attrib['href'])
            if page.xpath('.//a[contains(@href,"youtube")]'):
                p.add_link(page.xpath('.//a[contains(@href, "youtube")]')[0].attrib['href'])
            yield p

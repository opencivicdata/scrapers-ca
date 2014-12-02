from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

import re

COUNCIL_PAGE = 'http://www.ville.saint-jean-sur-richelieu.qc.ca/conseil-municipal/membres-conseil/Pages/membres-conseil.aspx'


class SaintJeanSurRichelieuPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//div[@class="article-content"]//td[@class="ms-rteTableOddCol-0"]')
        yield self.scrape_mayor(councillors[0])
        for councillor in councillors[1:]:
            if not councillor.xpath('.//a'):
                continue

            name = councillor.xpath('.//a')[0].text_content().strip()
            district = councillor.xpath('.//a')[1].text_content()
            url = councillor.xpath('.//a/@href')[0]
            page = self.lxmlize(url)

            p = Person(primary_org='legislature', name=name, district=district, role='Conseiller')
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)

            p.image = councillor.xpath('./preceding-sibling::td//img/@src')[-1]

            contacts = page.xpath('.//td[@class="ms-rteTableOddCol-0"]//text()')
            for contact in contacts:
                if re.findall(r'[0-9]', contact):
                    phone = contact.strip().replace(' ', '-')
                    p.add_contact('voice', phone, 'legislature')
            get_links(p, page.xpath('.//td[@class="ms-rteTableOddCol-0"]')[0])

            email = self.get_email(page)
            p.add_contact('email', email)
            yield p

    def scrape_mayor(self, div):
        name = div.xpath('.//a')[0].text_content()
        url = div.xpath('.//a/@href')[0]
        page = self.lxmlize(url)
        contact_url = page.xpath('//a[@title="Joindre le maire"]/@href')[0]
        contact_page = self.lxmlize(contact_url)

        p = Person(primary_org='legislature', name=name, district='Saint-Jean-sur-Richelieu', role='Maire')
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)
        p.add_source(contact_url)

        p.image = div.xpath('./preceding-sibling::td//img/@src')[-1]

        contacts = contact_page.xpath('//div[@id="ctl00_PlaceHolderMain_ctl01_ctl01__ControlWrapper_RichHtmlField"]//font/text()')
        address = ' '.join(contacts[:4])
        phone = contacts[-3].split(':')[1].strip().replace(' ', '-')
        fax = contacts[-2].split(':')[1].strip().replace(' ', '-')
        p.add_contact('address', address, 'legislature')
        p.add_contact('voice', phone, 'legislature')
        p.add_contact('fax', fax, 'legislature')
        # mayor's email is a form
        return p


def get_links(councillor, div):
    links = div.xpath('.//a')
    for link in links:
        link = link.attrib['href']

        if 'mailto:' in link:
            continue
        else:
            councillor.add_link(link)

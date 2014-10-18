from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

import re

COUNCIL_PAGE = 'http://guelph.ca/city-hall/mayor-and-council/city-council/'


class GuelphPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//*[@class="two_third last"]')
        for councillor in councillors:
            if councillor == councillors[0]:
                yield self.scrape_mayor(councillor)
                continue

            name = councillor.xpath('.//a')[0].text_content().replace('Councillor', '').replace('Mayor', '')
            info = councillor.xpath('.//text()[normalize-space()]')
            district = info[2]
            url = councillor.xpath('.//a')[0].attrib['href']

            p = Person(primary_org='legislature', name=name, district=district, role='Councillor')
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)

            p.add_contact('voice', info[3].replace('extension', 'x'), 'legislature')
            email = councillor.xpath('.//a[contains(@href,"mailto:")]')
            if email:
                email = email[0].text_content()
                p.add_contact('email', email)

            site = councillor.xpath('.//a[contains(text(),"Website")]')
            if site:
                p.add_link(site[0].attrib['href'])

            page = self.lxmlize(url)

            p.image = page.xpath('//header/img/@src')[0]

            address = re.findall(r'Address: (.*)Phone', page.xpath('//div[@class="entry-content"]')[0].text_content())
            if address:
                p.add_contact('address', address[0], 'legislature')

            blog = page.xpath('//a[contains(text(),"Blog")]')
            if blog:
                p.add_link(blog[0].attrib['href'])

            facebook = page.xpath('//div[@class="entry-content"]//a[contains(@href, "facebook")]')
            if facebook:
                p.add_link(facebook[0].attrib['href'])
            twitter = page.xpath('//div[@class="entry-content"]//a[contains(@href, "twitter")]')
            if twitter:
                p.add_link(twitter[0].attrib['href'])
            yield p

    def scrape_mayor(self, div):
        name = div.xpath('.//a')[0].text_content().replace('Mayor', '')
        url = div.xpath('.//a')[0].attrib['href']

        p = Person(primary_org='legislature', name=name, district='Guelph', role='Mayor')
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)

        phone = div.xpath('.//text()[normalize-space()]')[2]
        email = div.xpath('.//a[contains(@href,"mailto:")]')[0].text_content()

        page = self.lxmlize(url)

        p.add_contact('voice', phone, 'legislature')
        p.add_contact('email', email)
        p.add_link(page.xpath('//div[@class="entry-content"]//a[contains(@href, "facebook")]')[0].attrib['href'])
        p.add_link(page.xpath('//div[@class="entry-content"]//a[contains(@href, "twitter")]')[0].attrib['href'])
        p.image = page.xpath('//header/img/@src')[0]

        return p

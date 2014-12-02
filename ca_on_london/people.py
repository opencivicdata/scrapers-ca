from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

import re

COUNCIL_PAGE = 'http://www.london.ca/city-hall/city-council/Pages/default.aspx'
MAYOR_PAGE = 'http://www.london.ca/city-hall/mayors-office/Pages/default.aspx'


class LondonPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        councillor_pages = page.xpath('//div[@class="imageLinkContent"]/a[starts-with(text(), "Ward")]/@href')

        for councillor_page in councillor_pages:
            yield self.councillor_data(councillor_page)

        mayor_page = self.lxmlize(MAYOR_PAGE)
        mayor_connecting_url = mayor_page.xpath('//a[@class="headingLink"][contains(text(), "Connecting")]/@href')[0]
        yield self.mayor_data(mayor_connecting_url)

    def councillor_data(self, url):
        page = self.lxmlize(url)

        name = page.xpath('//h1[@id="TitleOfPage"]//text()')[0]
        district = page.xpath('//h2//text()')[0]

        # TODO: Councillor emails are built with JS to prevent scraping, but the JS can be scraped.

        address = page.xpath('//div[@class="asideContent"]//text()')[0]

        photo = page.xpath('//div[@id="contentright"]//img[1]/@src')[0]
        phone = get_phone_data(page)

        js = page.xpath('string(//span/script)')  # allow string()
        email = email_js(js)

        p = Person(primary_org='legislature', name=name, district=district, role='Councillor')
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)
        p.add_contact('address', address, 'legislature')
        p.add_contact('voice', phone, 'legislature')
        p.add_contact('email', email)
        p.image = photo

        return p

    def mayor_data(self, url):
        page = self.lxmlize(url)

        name = page.xpath('//h1[@id="TitleOfPage"]//text()')[0].split('Mayor')[-1]
        photo_url = page.xpath('//div[@class="imageLeftDiv"]/img/@src')[0]
        phone = get_phone_data(page)

        js = page.xpath('string(//span/script)')  # allow string()
        email = email_js(js)

        phone_str = page.xpath('//span[contains(@class, "iconPhone")]//text()')[0]
        phone = phone_str.split(':')[1]

        p = Person(primary_org='legislature', name=name, district='London', role='Mayor')
        p.add_source(MAYOR_PAGE)
        p.add_source(url)
        p.image = photo_url
        p.add_contact('email', email)
        p.add_contact('voice', phone, 'legislature')
        return p


def get_phone_data(page):
    # We search for "hone" because the first "p" can change case... oh, xpath.
    # We also only return the first phone number we get. There's no consistency.
    phone_text = page.xpath('(//span[contains(@class, "contactValue")]//text()[contains(., "hone")])[1]')[0]
    return re.search(r'[0-9].*$', phone_text).group()


def email_js(js):
    user, domain, suffix = re.findall(r'trim\("(.+?)"', js)[:3]
    email = user + '@' + domain + '.' + suffix
    return email

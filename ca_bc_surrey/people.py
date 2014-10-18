from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.surrey.ca/city-government/2999.aspx'


class SurreyPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        councillor_links = page.xpath(
            '//div[@class="inner-wrapper"]//a[contains(text(), "Councillor")]')
        for link in councillor_links:
            role, name = link.text.split(' ', 1)
            url = link.attrib['href']
            councillor_page = self.lxmlize(url)
            photo_url = councillor_page.xpath(
                'string(.//div[@class="inner-wrapper"]//img/@src)')
            phone = councillor_page.xpath(
                'string(//text()[contains(., "hone:")][1])')
            email = councillor_page.xpath(
                'string(//a[contains(@href, "mailto:")])')

            p = Person(primary_org='legislature', name=name, district='Surrey', role=role, image=photo_url)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)
            if phone:
                p.add_contact('voice', phone, 'legislature')
            p.add_contact('email', email)
            yield p

        mayor_link = page.xpath(
            '//div[@class="inner-wrapper"]//a[contains(text(), "Mayor")]')[0]
        mayor_url = mayor_link.attrib['href']
        name = mayor_link.text.split(' ', 2)[1]
        mayor_page = self.lxmlize(mayor_url)
        photo_url = mayor_page.xpath('string(//img[contains(@src, "Mayor")]/@src)')
        phone = mayor_page.xpath('string(//text()[contains(., "Office:")])')
        # no email

        p = Person(primary_org='legislature', name=name, district='Surrey', role='Mayor', image=photo_url)
        p.add_source(COUNCIL_PAGE)
        p.add_source(mayor_url)
        p.add_contact('voice', phone, 'legislature')
        yield p

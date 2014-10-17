# coding: utf-8
from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.mississauga.ca/portal/cityhall/mayorandcouncil'
MAYOR_PAGE = 'http://www.mississauga.ca/portal/cityhall/contactthemayor'


class MississaugaPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillor_urls = page.xpath('//area/@href')[1:]

        for councillor_url in councillor_urls:
            yield self.councillor_data(councillor_url)

        yield self.mayor_data(MAYOR_PAGE)

    def councillor_data(self, url):
        page = self.lxmlize(url)

        name = page.xpath('string(//strong[1]/text())')
        district = page.xpath('string(//span[@class="pageHeader"])')
        email = page.xpath('string(//div[@class="blockcontentclear"]//a/'
                           '@href[contains(., "@")][1])')
        photo = page.xpath('string(//div[@class="blockcontentclear"]//img[1]/@src)')

        p = Person(primary_org='legislature', name=name, district=district, role='Councillor')
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)
        p.add_contact('email', email)
        p.image = photo

        return p

    def mayor_data(self, url):
        page = self.lxmlize(url)

        # TODO: Consider getting photo. It's on a separate page.
        name_text = page.xpath('//p[contains(text(), "Worship Mayor")]/text()')[0]
        name = ' '.join(name_text.split()[3:])  # TODO: probably too brittle
        email = page.xpath('//a[contains(@href, "mailto")]/text()')[0]

        p = Person(primary_org='legislature', name=name, district='Mississauga', role='Mayor')
        p.add_source(url)
        p.add_contact('email', email)

        return p

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

        name = page.xpath('//strong[2]/text()')[0]
        district = page.xpath('//span[@class="pageHeader"]//text()')[0]
        email = self.get_email(page, '//div[@class="blockcontentclear"]')
        photo = page.xpath('//div[@class="blockcontentclear"]//img[1]/@src')[0]

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
        email = self.get_email(page)

        p = Person(primary_org='legislature', name=name, district='Mississauga', role='Mayor')
        p.add_source(url)
        p.add_contact('email', email)

        return p

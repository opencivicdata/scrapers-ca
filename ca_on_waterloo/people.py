from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.waterloo.ca/en/government/aboutmayorandcouncil.asp'


class WaterlooPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillor_pages = page.xpath('//div[@id="subNavContainer"]//li/a[contains(@title, "Coun.")]/@href')

        for councillor_page in councillor_pages:
            yield self.councillor_data(councillor_page)

        mayor_url = page.xpath('(//div[@id="subNavContainer"]//li//li//li/a)[1]/@href')[0]
        yield self.mayor_data(mayor_url)

    def photo_url(self, page):
        return page.xpath('//div[@id="printAreaContent"]/p/img/@src')[0]

    def councillor_data(self, url):
        page = self.lxmlize(url)

        # Eliminate the "Coun." From the page title and get name and district
        name, district = page.xpath('//h1//text()')[0][6:].split('-')

        # Email is handled as a form and no contact information is listed

        p = Person(primary_org='legislature', name=name, district=district, role='Councillor')
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)
        p.image = self.photo_url(page)

        return p

    def mayor_data(self, url):
        page = self.lxmlize(url)

        # Eliminate the word "Mayor" preceding the Mayor's name
        name = page.xpath('//h1')[0][6:]
        p = Person(primary_org='legislature', name=name, district='Waterloo', role='Mayor')
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)
        p.image = self.photo_url(page)

        return p

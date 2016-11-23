from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

from six.moves.urllib.parse import urljoin

COUNCIL_PAGE = 'http://www.regina.ca/residents/council-committees/meet-city-council/'
MAYOR_CONTACT_URL = 'http://www.regina.ca/residents/regina-mayor/contact_mayor'


class ReginaPersonScraper(CanadianScraper):

    def scrape(self):
        root = self.lxmlize(COUNCIL_PAGE)

        councillor_links = root.xpath('//div[@id="right_col"]//li[contains(., "Ward")]/a')
        for link in councillor_links:
            text = link.xpath('.//text()')[0]
            ward, name = text.split(' - Councillor ')
            url = link.xpath('./@href')[0]
            yield self.councillor_data(url, name, ward)

        mayor_link = root.xpath('//div[@id="right_col"]//li[contains(., "Mayor")]/a')[0]
        mayor_name = mayor_link.text_content()[len('Mayor '):]
        mayor_url = mayor_link.xpath('./@href')[0]
        yield self.mayor_data(mayor_url, mayor_name)

    def councillor_data(self, url, name, ward):
        page = self.lxmlize(url)
        # sadly, email is a form on a separate page
        photo_url_rel = page.xpath('//div[contains(@id, "contentcontainer")]//img/@src')[0]
        photo_url = urljoin(url, photo_url_rel)

        m = Person(primary_org='legislature', name=name, district=ward, role='Councillor')
        m.add_source(COUNCIL_PAGE)
        m.add_source(url)

        phone = self.get_phone(page.xpath('//div[@id="contentcontainer"]')[0], area_codes=[306], error=False)
        if phone:
            m.add_contact('voice', phone, 'legislature')

        m.image = photo_url
        yield m

    def mayor_data(self, url, name):
        page = self.lxmlize(url)
        photo_url = urljoin(url,
                            page.xpath('(//div[@id="contentcontainer"]//img)[1]/@src')[0])

        m = Person(primary_org='legislature', name=name, district='Regina', role='Mayor')
        m.add_source(COUNCIL_PAGE)
        m.add_source(url)
        m.image = photo_url

        return m

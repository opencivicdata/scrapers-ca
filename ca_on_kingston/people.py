from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

from six.moves.urllib.parse import urljoin

COUNCIL_PAGE = 'http://www.cityofkingston.ca/city-hall/city-council/mayor-and-council'


class KingstonPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        mayor_and_council_urls = page.xpath('//ul[@class="no-list no-margin"]//ul[@class="no-list no-margin"]//li/a/@href')
        mayor_url = mayor_and_council_urls[0]
        council_urls = mayor_and_council_urls[1:]

        for councillor_url in council_urls:
            yield self.councillor_data(councillor_url)

        yield self.mayor_data(mayor_url)

    def councillor_data(self, url):
        page = self.lxmlize(url)

        # largely based on old scraper
        contact_node = page.xpath('//div[text()[contains(.,"Phone:")]]')[0]

        name = contact_node.xpath('./span[1]//text()')[0]
        district = contact_node.xpath('./text()[2]')[0]
        district_id = district.split(':')[0]  # TODO: don't reject name?
        email = self.get_email(contact_node)
        phone = self.get_phone(contact_node, [343, 613])
        photo_url_rel = page.xpath('.//img[@class="innerimage"]/@src')[0]
        photo_url = urljoin(url, photo_url_rel)

        p = Person(primary_org='legislature', name=name, district=district_id, role='Councillor')
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)
        p.add_contact('email', email)
        if phone:
            p.add_contact('voice', phone, 'legislature')
        p.image = photo_url

        return p

    def mayor_data(self, url):
        page = self.lxmlize(url)

        # largely based on old scraper
        contact_node = page.xpath('//div[text()[contains(.,"Phone:")]]')[0]

        name = contact_node.xpath('./span[1]//text()')[0]
        email = self.get_email(contact_node)
        photo_url = page.xpath('//img[@class="innerimage"]/@src')[0]

        p = Person(primary_org='legislature', name=name, district='Kingston', role='Mayor')
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)
        p.add_contact('email', email)
        p.image = photo_url

        return p

import re

from utils import CanadianScraper, CanadianPerson as Person

from urllib.parse import urljoin

COUNCIL_PAGE = 'https://www.regina.ca/city-government/city-council'
MAYOR_CONTACT_URL = 'https://www.regina.ca/city-government/city-council/mayors-office'


class ReginaPersonScraper(CanadianScraper):
    def scrape(self):
        root = self.lxmlize(COUNCIL_PAGE)

        councillors = root.xpath('//div[@id="navigation-navigation"]//li//ul//li[contains(., "Ward")]/a')
        assert len(councillors), 'No councillors found'
        for link in councillors:
            text = link.xpath('.//text()')[0]
            ward, name = text.split(' - Councillor ')
            url = link.xpath('./@href')[0]
            yield self.councillor_data(url, name, ward)

        mayor_link = root.xpath('//div[@id="navigation-navigation"]//li[contains(., "Mayor")]/a')[0]
        mayor_url = mayor_link.xpath('./@href')[0]
        yield self.mayor_data(mayor_url)

    def councillor_data(self, url, name, ward):
        page = self.lxmlize(url)
        # sadly, email is a form on a separate page
        photo_url_rel = page.xpath('//div[@class="councillor__image"]//img/@src')[0]
        photo_url = urljoin(url, photo_url_rel)

        m = Person(primary_org='legislature', name=name, district=ward, role='Councillor')
        m.add_source(COUNCIL_PAGE)
        m.add_source(url)

        # Scrape and add phone.
        phone_path = page.xpath('//div[@class="councillor__contact"]//ul/li/a/@href[contains(., "306")]')[0]
        phone_string = phone_path.rsplit('/', 1)[-1]
        phone = re.sub('[^0-9]','', phone_string)
        if phone:
            m.add_contact('voice', phone, 'legislature')

        m.image = photo_url
        yield m

    def mayor_data(self, url):
        page = self.lxmlize(url)

        name = page.xpath('//div[@class="councillor__name"]//h1/text()')[0]

        photo_url_rel = page.xpath('//div[@class="councillor__image"]//img/@src')[0]
        photo_url = urljoin(url, photo_url_rel)

        m = Person(primary_org='legislature', name=name, district='Regina', role='Mayor')
        m.add_source(COUNCIL_PAGE)
        m.add_source(url)
        m.image = photo_url

        # Scrape and add phone.
        phone_path = page.xpath('//div[@class="councillor__contact"]//ul/li/a/@href[contains(., "306")]')[0]
        phone_string = phone_path.rsplit('/', 1)[-1]
        phone = re.sub('[^0-9]','', phone_string)
        if phone:
            m.add_contact('voice', phone, 'legislature')

        return m

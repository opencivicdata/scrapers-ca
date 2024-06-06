from urllib.parse import urljoin

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.regina.ca/city-government/city-council"
MAYOR_CONTACT_URL = "https://www.regina.ca/city-government/city-council/mayors-office/contact-mayor/"


class ReginaPersonScraper(CanadianScraper):
    def scrape(self):
        root = self.lxmlize(COUNCIL_PAGE)

        councillors = root.xpath('//div[@id="navigation-navigation"]//li//ul//li[contains(., "Ward")]/a')
        assert len(councillors), "No councillors found"
        for link in councillors:
            text = link.xpath(".//text()")[0]
            ward, name = text.split(" - Councillor ")
            url = link.xpath("./@href")[0]
            yield self.councillor_data(url, name, ward)

        mayor_link = root.xpath('//div[@id="navigation-navigation"]//li[contains(., "Mayor")]/a')[0]
        mayor_url = mayor_link.xpath("./@href")[0]
        yield self.mayor_data(mayor_url)

    def councillor_data(self, url, name, ward):
        page = self.lxmlize(url)
        photo_url_rel = page.xpath('//div[@class="councillor__image"]//img/@src')[0]
        photo_url = urljoin(url, photo_url_rel)

        m = Person(primary_org="legislature", name=name, district=ward, role="Councillor")
        m.add_source(COUNCIL_PAGE)
        m.add_source(url)

        m.add_contact("voice", self.get_phone(page), "legislature")
        m.add_contact("email", self.get_email(page))

        m.image = photo_url
        yield m

    def mayor_data(self, url):
        page = self.lxmlize(url)

        name = page.xpath('//div[@class="councillor__name"]//h1/text()')[0]

        photo_url_rel = page.xpath('//div[@class="councillor__image"]//img/@src')[0]
        photo_url = urljoin(url, photo_url_rel)

        m = Person(primary_org="legislature", name=name, district="Regina", role="Mayor")
        m.add_source(COUNCIL_PAGE)
        m.add_source(url)
        m.image = photo_url

        page = self.lxmlize(MAYOR_CONTACT_URL)
        m.add_contact("voice", self.get_phone(page), "legislature")
        m.add_contact("email", self.get_email(page))

        return m

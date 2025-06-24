import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_URL = "https://www.saskatoon.ca/city-hall/mayor-city-councillors/city-councillors-wards"
MAYOR_URL = "https://www.saskatoon.ca/city-hall/mayor-city-councillors/mayors-office"


class SaskatoonPersonScraper(CanadianScraper):
    def scrape(self):
        yield self.scrape_mayor()

        page = self.lxmlize(COUNCIL_URL)

        councillors = page.xpath('//h2[@class="landing-block-title"]/a/@href')

        assert len(councillors), "No councillors found"
        for url in councillors:
            page = self.lxmlize(url)
            content = page.xpath('//div[@id="main-content"]')[0]

            district = content.xpath(".//h1")[0].text_content()
            name = content.xpath(".//h2")[0].text_content().replace("Councillor:", "").strip()
            image = content.xpath(".//img/@src")[0]

            p = Person(primary_org="legislature", name=name, district=district, role="Councillor", image=image)

            contact_node = page.xpath('//aside[@class="page-sidebar"]')[0]
            phone = self.get_phone(contact_node)

            p.add_contact("voice", phone, "legislature")
            p.add_source(COUNCIL_URL)
            yield p

    def scrape_mayor(self):
        page = self.lxmlize(MAYOR_URL)
        info = page.xpath('//div[@id="main-content"]//div[contains(@class, "field--name-body")]/p')[0].text_content()
        name = re.search(r"Mayor [A-Z]\w+ [A-Z]\w+", info)
        assert name is not None, "Could not find Mayor name"
        name = name.group(0)

        p = Person(primary_org="legislature", name=name, district="Saskatoon", role="Mayor")

        contact_node = page.xpath('//aside[@class="page-sidebar"]')[0]
        phone = self.get_phone(contact_node)

        p.add_contact("voice", phone, "legislature")
        p.add_source(MAYOR_URL)
        yield p

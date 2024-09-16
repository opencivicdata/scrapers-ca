import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.oakville.ca/town-hall/mayor-council-administration/mayor-council/"


class OakvillePersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//div[@class="card h-100"]')
        assert len(councillors), "No councillors found"

        for councillor in councillors:
            district_role = councillor.xpath(".//div[@class='user-function']/text()")[0]
            if "Mayor" in district_role:
                district = "Oakville"
                role = district_role
            else:
                district, role = re.split(r"(?<=\d)\s+", district_role, maxsplit=1)
                role = "Regional Councillor" if "Regional" in role else "Councillor"

            name = councillor.xpath(".//div[@class='user-name']/text()")[0]
            email = self.get_email(councillor)
            phone = self.get_phone(councillor)
            url = councillor.xpath('.//a[@class="btn"]/@href')[0]

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.image = councillor.xpath(".//img/@src")[0]

            p.add_contact("email", email)
            p.add_contact("voice", phone, "legislature")

            p.add_source(COUNCIL_PAGE)
            p.add_source(url)

            yield p

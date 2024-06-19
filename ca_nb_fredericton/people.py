import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.fredericton.ca/en/your-government/mayor-council"


class FrederictonPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath(
            '//div[contains(@class, "field field--name-field-content-rows field--type-entity-reference-revisions field--label-hidden content-rows field__items")]//div[contains(@class, "views-row")]'
        )
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            name = councillor.xpath(".//h3/a")[0].text_content()
            text = councillor.xpath('.//div[@class="views-field views-field-field-councillor-title"]/div')[
                0
            ].text_content()
            ward = re.findall(r"Ward \d+", text)
            if ward:
                district = ward[0]
                role = "Councillor"
            else:
                district = "Fredericton"
                role = "Mayor"

            url = councillor.xpath(".//@href")[0]
            page = self.lxmlize(url)

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)

            p.image = councillor.xpath('.//img[@typeof="foaf:Image"]/@src')[0]
            p.add_contact("email", self.get_email(page))
            p.add_contact("voice", self.get_phone(page, area_codes=[506]), "legislature")

            yield p

import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

BASE_URL = "https://www.barrie.ca/government/council-committees/city-council"
COUNCIL_PAGES = [f"{BASE_URL}/mayor", *(f"{BASE_URL}/councillor-{ward_number}" for ward_number in range(1, 11))]


class BarriePersonScraper(CanadianScraper):
    def scrape(self):
        for url in COUNCIL_PAGES:
            page = self.lxmlize(url)
            article = page.xpath('//article[contains(@class, "node--type-city-council-member")]')[0]

            name = page.xpath("//h1//text()")[0].strip()
            position = article.xpath('.//div[contains(@class, "field--name-field-name")]')[0].text_content().strip()
            ward_match = re.match(r"Ward (\d+) Councillor", position)

            if position == "Mayor of Barrie":
                role = "Mayor"
                district = "Barrie"
            elif ward_match:
                role = "Councillor"
                district = f"Ward {ward_match.group(1)}"
            else:
                raise ValueError(f"Unexpected position: {position}")

            image = article.xpath('.//div[contains(@class, "field--name-field-image")]//img/@src')

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(url)
            p.add_contact("voice", self.get_phone(article), "legislature")
            p.add_contact("email", self.get_email(article))
            if image:
                p.image = image[0]

            yield p

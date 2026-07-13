import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.saint-georges.ca/ville/vie-democratique/conseil-de-ville"


class SaintGeorgesPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        members = page.xpath('//div[contains(@class, "rubric__text")][.//h2[contains(@class, "rubric__title")]]')
        assert len(members) == 9, "Expected 9 council members"

        for member in members:
            text = [text.strip() for text in member.xpath(".//text()") if text.strip()]
            name = text[1] if len(text) > 1 else text[0]
            name = re.sub(r",?\s+mairesse$", "", name)
            name = re.sub(r"^(?:M\.|Mme\.?)\s+", "", name)
            if "Mairesse" in text[0]:
                role = "Maire"
                district = "Saint-Georges"
            else:
                role = "Conseiller"
                district_number = re.search(r"\d+", text[0]).group(0)
                district = f"District {district_number}"

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            email = self.get_email(member, error=False)
            if email:
                p.add_contact("email", email)
            yield p

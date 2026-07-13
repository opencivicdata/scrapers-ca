import re
from urllib.parse import urljoin

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.st-hyacinthe.ca/ville/vie-democratique/conseil-municipal"


class SaintHyacinthePersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        members = page.xpath(
            '//div[contains(@class, "wow") and contains(@class, "fadeInUp")][.//a[contains(@href, "mailto:")]]'
        )
        assert len(members) == 11, "Expected 11 council members"

        for member in members:
            text = [text.strip() for text in member.xpath(".//text()") if text.strip()]
            name = text[0]

            if text[1] == "Maire":
                role = "Maire"
                district = "Saint-Hyacinthe"
            else:
                role = "Conseiller"
                district = f"{text[1]} - {text[2]}"

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            image = member.xpath(".//img/@src")
            if image:
                p.image = urljoin(COUNCIL_PAGE, image[0])

            email = self.get_email(member, error=False)
            if email:
                p.add_contact("email", email)

            phone = self.get_phone(member, area_codes=[438, 450, 514, 579], error=False)
            if phone:
                phone = re.sub(r"\s+", " ", phone)
                p.add_contact("voice", phone, "legislature")

            yield p

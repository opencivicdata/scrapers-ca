import re
from urllib.parse import urljoin

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://mirabel.ca/conseil-municipal"


class MirabelPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        members = page.xpath('//a[contains(@href, "/conseil-municipal/")][.//img]')
        assert len(members) == 11, "Expected 11 council members"

        for member in members:
            text = [text.strip() for text in member.xpath(".//text()") if text.strip()]
            url = urljoin(COUNCIL_PAGE, member.get("href"))
            detail_page = self.lxmlize(url)

            if text[0] == "Mairesse":
                role = "Mairesse"
                name = text[1]
                district = "Mirabel"
            else:
                role = "Conseiller"
                district = f"District {text[0]}"
                name = text[2]

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)

            image = member.xpath(".//img/@src")
            if image:
                p.image = urljoin(COUNCIL_PAGE, image[0])

            email = self.get_email(detail_page, error=False)
            if email:
                p.add_contact("email", email)

            phone = self.get_phone(detail_page, area_codes=[438, 450, 514, 579, 819], error=False)
            if phone:
                phone = re.sub(r"\s+", " ", phone)
                p.add_contact("voice", phone, "legislature")

            yield p

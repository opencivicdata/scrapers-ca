import re
from urllib.parse import urljoin

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.mapleridge.ca/your-government/city-council/meet-your-council"


class MapleRidgePersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        members = page.xpath('//div[contains(@class, "views-row") and contains(@class, "list-item")]')
        assert len(members) == 7, "Expected 7 council members"

        councillor_seat_number = 1
        for member in members:
            title = member.xpath('normalize-space(.//h3[contains(@class, "list-item__title")]/a)')
            role, name = title.split(" ", 1)
            name = re.sub(r"\s+\(.*\)$", "", name)

            if role == "Mayor":
                district = "Maple Ridge"
            else:
                district = f"Maple Ridge (seat {councillor_seat_number})"
                councillor_seat_number += 1

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            url = member.xpath('.//h3[contains(@class, "list-item__title")]/a/@href')
            if url:
                p.add_source(url[0])

            image = member.xpath(".//img/@src")
            if image:
                p.image = urljoin(COUNCIL_PAGE, image[0])

            email = self.get_email(member, error=False)
            if email:
                p.add_contact("email", email)

            phone = self.get_phone(member, area_codes=[604, 778], error=False)
            if phone:
                p.add_contact("voice", phone, "legislature")

            yield p

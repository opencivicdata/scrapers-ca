from urllib.parse import urljoin

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.airdrie.ca/index.cfm?serviceID=2169"


class AirdriePersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        members = page.xpath(
            '//div[contains(concat(" ", normalize-space(@class), " "), " content_item_display ")]'
            '[.//h2[starts-with(normalize-space(), "Mayor") or starts-with(normalize-space(), "Councillor")]]'
        )
        assert len(members) == 7, "Expected 7 council members"

        councillor_seat_number = 1
        for member in members:
            title = member.xpath("normalize-space(.//h2)")
            role, name = title.split(" ", 1)

            if role == "Mayor":
                district = "Airdrie"
            else:
                district = f"Airdrie (seat {councillor_seat_number})"
                councillor_seat_number += 1

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            image = member.xpath(".//img/@src")
            if image:
                p.image = urljoin(COUNCIL_PAGE, image[0])

            email = self.get_email(member, error=False)
            if email:
                p.add_contact("email", email)

            phone = self.get_phone(member, area_codes=[403, 587, 780, 825, 368], error=False)
            if phone:
                p.add_contact("voice", phone, "legislature")

            yield p

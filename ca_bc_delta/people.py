from urllib.parse import urljoin

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.delta.ca/city-hall/delta-council/delta-council-members"


class DeltaPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        members = page.xpath(
            '//div[contains(concat(" ", normalize-space(@class), " "), " m-accordion ")]'
            '[.//button[contains(normalize-space(.), "Mayor ") or contains(normalize-space(.), "Councillor ")]]'
        )
        assert len(members) == 7, "Expected 7 council members"

        councillor_seat_number = 1
        for member in members:
            title = member.xpath('.//button[contains(@class, "m-accordion__trigger")]')[0].text_content().strip()
            role, name = title.split(" ", 1)

            if role == "Mayor":
                district = "Delta"
            else:
                district = f"Delta (seat {councillor_seat_number})"
                councillor_seat_number += 1

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            image = member.xpath(".//img/@src")
            if image:
                p.image = urljoin(COUNCIL_PAGE, image[0])

            email = self.get_email(member)
            if email:
                p.add_contact("email", email)

            phone = self.get_phone(member, area_codes=[604, 778])
            if phone:
                p.add_contact("voice", phone, "legislature")

            yield p

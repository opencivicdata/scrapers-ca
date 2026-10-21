from urllib.parse import urljoin

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.princegeorge.ca/city-hall/mayor-council/council-members"


class PrinceGeorgePersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        members = page.xpath(
            '//div[contains(concat(" ", normalize-space(@class), " "), " paragraph--type--accordion-item ")]'
            '[.//div[contains(@class, "field--name-field-title")]'
            '[starts-with(normalize-space(), "Mayor") or starts-with(normalize-space(), "Councillor")]]'
        )
        assert len(members) == 9, "Expected 9 council members"

        councillor_seat_number = 1
        for member in members:
            title = member.xpath('normalize-space(.//div[contains(@class, "field--name-field-title")])')
            role, name = title.split(" ", 1)

            if role == "Mayor":
                district = "Prince George"
            else:
                district = f"Prince George (seat {councillor_seat_number})"
                councillor_seat_number += 1

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            image = member.xpath('.//img[contains(@src, "/sites/default/files/")]/@src')
            if image:
                p.image = urljoin(COUNCIL_PAGE, image[0])

            email = self.get_email(member, error=False)
            if email:
                p.add_contact("email", email)

            phone = self.get_phone(member, area_codes=[250, 236, 778, 672], error=False)
            if phone:
                p.add_contact("voice", phone, "legislature")

            yield p

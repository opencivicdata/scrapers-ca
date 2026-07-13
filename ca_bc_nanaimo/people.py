from urllib.parse import urljoin

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.nanaimo.ca/your-government/city-council/contact-mayor-and-council"


class NanaimoPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        members = page.xpath(
            '//div[contains(concat(" ", normalize-space(@class), " "), " sf_cols ")]'
            '[.//img and .//a[contains(@href, "mailto:")] and .//strong[normalize-space()]]'
        )
        assert len(members) == 9, "Expected 9 council members"

        councillor_seat_number = 1
        for index, member in enumerate(members):
            name = member.xpath("normalize-space(.//strong[normalize-space()][last()])")
            if index == 0:
                role = "Mayor"
                district = "Nanaimo"
            else:
                role = "Councillor"
                district = f"Nanaimo (seat {councillor_seat_number})"
                councillor_seat_number += 1

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            image = member.xpath(".//img/@src")
            if image:
                p.image = urljoin(COUNCIL_PAGE, image[0])

            email = self.get_email(member)
            if email:
                p.add_contact("email", email)

            phone = self.get_phone(member, area_codes=[250])
            if phone:
                p.add_contact("voice", phone, "legislature")

            yield p

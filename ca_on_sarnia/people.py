from urllib.parse import urljoin

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://sarnia.civicweb.net/portal/members.aspx?id=8"


class SarniaPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        members = page.xpath('//div[contains(concat(" ", normalize-space(@class), " "), " item-template ")][.//h2]')
        assert len(members) == 9, "Expected 9 council members"

        councillor_seat_number = 1
        for member in members:
            name = member.xpath("normalize-space(.//h2)")
            text = [text.strip() for text in member.xpath(".//text()") if text.strip()]
            title = text[2]

            if title == "Mayor":
                role = "Mayor"
                district = "Sarnia"
            else:
                role = "Councillor"
                district = f"Sarnia (seat {councillor_seat_number})"
                councillor_seat_number += 1

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            image = member.xpath(".//img/@src")
            if image:
                p.image = urljoin(COUNCIL_PAGE, image[0])

            email = self.get_email(member, error=False)
            if email:
                p.add_contact("email", email)

            phone = self.get_phone(member, area_codes=[226, 519, 548], error=False)
            if phone:
                p.add_contact("voice", phone, "legislature")

            yield p

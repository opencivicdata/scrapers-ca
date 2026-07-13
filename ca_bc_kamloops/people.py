from urllib.parse import urljoin

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://kamloops.civicweb.net/portal/members.aspx?id=26"

FULL_NAMES = {
    "Mayor Hamer-Jackson": "Reid Hamer-Jackson",
    "Councillor Bass": "Dale Bass",
    "Councillor Bepple": "Nancy Bepple",
    "Councillor Hall": "Kelly Hall",
    "Councillor Karpuk": "Stephen Karpuk",
    "Councillor Middleton": "Margot Middleton",
    "Councillor Neustaeter": "Katie Neustaeter",
    "Councillor O'Reilly": "Mike O'Reilly",
    "Councillor Sarai": "Bill Sarai",
}


class KamloopsPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        members = page.xpath(
            '//div[contains(concat(" ", normalize-space(@class), " "), " item-template ")]'
            '[.//h2[starts-with(normalize-space(), "Mayor") or starts-with(normalize-space(), "Councillor")]]'
        )
        assert len(members) == 9, "Expected 9 council members"

        councillor_seat_number = 1
        for member in members:
            title = member.xpath("normalize-space(.//h2)")
            if title.startswith("Mayor "):
                role = "Mayor"
                district = "Kamloops"
            else:
                role = "Councillor"
                district = f"Kamloops (seat {councillor_seat_number})"
                councillor_seat_number += 1

            p = Person(primary_org="legislature", name=FULL_NAMES[title], district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            image = member.xpath(".//img/@src")
            if image and image[0]:
                p.image = urljoin(COUNCIL_PAGE, image[0])

            email = self.get_email(member, error=False)
            if email:
                p.add_contact("email", email)

            phone = self.get_phone(member, area_codes=[250, 236, 778, 672], error=False)
            if phone:
                p.add_contact("voice", phone, "legislature")

            yield p

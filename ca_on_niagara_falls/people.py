from urllib.parse import urljoin

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://niagarafalls.ca/city-government/city-council-and-mayor/"


class NiagaraFallsPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        members = page.xpath(
            '//div[contains(@class, "text") and contains(@class, "base-text")]'
            '[.//a[contains(@href, "mailto:") and not(contains(@href, "service@"))]]'
        )
        assert len(members) == 9, "Expected 9 council members"

        councillor_seat_number = 1
        for member in members:
            name = member.xpath('normalize-space(.//a[contains(@href, "mailto:")])')
            if name.startswith("Mayor "):
                role = "Mayor"
                name = name.replace("Mayor ", "", 1)
                district = "Niagara Falls"
            else:
                role = "Councillor"
                district = f"Niagara Falls (seat {councillor_seat_number})"
                councillor_seat_number += 1

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            image = member.xpath("ancestor::*[.//img][1]//img/@src")
            if image:
                p.image = urljoin(COUNCIL_PAGE, image[0])

            email = self.get_email(member)
            if email:
                p.add_contact("email", email)

            phone = self.get_phone(member, area_codes=[289, 905])
            if phone:
                p.add_contact("voice", phone, "legislature")

            yield p

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.stratford.ca/inside-city-hall/city-council/city-council-contact/"


class StratfordPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        members = page.xpath('//td[.//img[starts-with(@alt, "Mayor ") or starts-with(@alt, "Councillor ")]]')
        assert len(members) == 11, "Expected 11 council members"

        seat_number = 1
        for member in members:
            title = member.xpath(
                "normalize-space(.//p/strong[starts-with(., 'Mayor ') or starts-with(., 'Councillor ')])"
            )
            role, name = title.split(" ", 1)
            if role == "Mayor":
                district = "Stratford"
            else:
                district = f"Stratford (seat {seat_number})"
                seat_number += 1

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.image = member.xpath(".//img/@src")[0]
            email = self.get_email(member, error=False)
            if email:
                p.add_contact("email", email)
            phone = self.get_phone(member, area_codes=[226, 519, 548], error=False)
            if phone:
                p.add_contact("voice", phone, "legislature")
            yield p

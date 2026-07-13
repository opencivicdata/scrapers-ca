from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.cochrane.ca/government/council"


class CochranePersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        members = page.xpath(
            '//div[contains(@class, "views-row")][.//h3[starts-with(., "Mayor") or starts-with(., "Councillor")]]'
        )
        assert len(members) == 7, "Expected 7 council members"

        seat_number = 1
        for member in members:
            title = member.xpath("normalize-space(.//h3)")
            role, name = title.split(" ", 1)
            if role == "Mayor":
                district = "Cochrane"
            else:
                district = f"Cochrane (seat {seat_number})"
                seat_number += 1

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            email = self.get_email(member, error=False)
            if email:
                p.add_contact("email", email)
            yield p

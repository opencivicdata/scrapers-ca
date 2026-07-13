from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.leduc.ca/government/mayor-council"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36"
)


class LeducPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, user_agent=USER_AGENT)
        members = page.xpath('//div[contains(@class, "personnel--card")][.//h5[contains(@class, "name")]]')
        assert len(members) == 7, "Expected 7 council members"

        seen = set()
        seat_number = 1
        for member in members:
            name = member.xpath('normalize-space(.//h5[contains(@class, "name")])')
            if name in seen:
                continue
            seen.add(name)
            role = member.xpath('normalize-space(.//p[contains(@class, "title")])')
            if role == "Mayor":
                district = "Leduc"
            else:
                role = "Councillor"
                district = f"Leduc (seat {seat_number})"
                seat_number += 1

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            image = member.xpath(".//img/@src")
            if image:
                p.image = image[0]
            email = self.get_email(member, error=False)
            if email:
                p.add_contact("email", email)

            yield p

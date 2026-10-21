from urllib.parse import urljoin

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://orillia.civicweb.net/portal/members.aspx?id=9"


class OrilliaPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        members = page.xpath('//div[contains(concat(" ", normalize-space(@class), " "), " item-template ")][.//h2]')
        assert len(members) == 9, "Expected 9 council members"

        seat_numbers = {}
        for member in members:
            name = member.xpath("normalize-space(.//h2)")
            title = [text.strip() for text in member.xpath(".//text()") if text.strip()][2]
            if title == "Mayor":
                role = "Mayor"
                district = "Orillia"
            else:
                role = "Councillor"
                ward = title.split(" - ", 1)[1]
                seat_numbers[ward] = seat_numbers.get(ward, 0) + 1
                district = f"{ward} (seat {seat_numbers[ward]})"

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            image = member.xpath(".//img/@src")
            if image:
                p.image = urljoin(COUNCIL_PAGE, image[0])
            email = self.get_email(member, error=False)
            if email:
                p.add_contact("email", email)
            yield p

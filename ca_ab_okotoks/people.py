from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.okotoks.ca/your-government/your-council/town-council"


class OkotoksPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        headings = page.xpath('//h2[contains(@class, "councillor__name")]')
        assert len(headings) == 7, "Expected 7 council members"

        seat_number = 1
        for heading in headings:
            role, name = heading.text_content().strip().split(" ", 1)
            if role == "Mayor":
                district = "Okotoks"
            else:
                district = f"Okotoks (seat {seat_number})"
                seat_number += 1

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            yield p

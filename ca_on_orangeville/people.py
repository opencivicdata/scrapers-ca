from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.orangeville.ca/en/town-hall/council.aspx"


class OrangevillePersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        headings = page.xpath(
            '//h3[starts-with(normalize-space(), "Mayor ") or starts-with(normalize-space(), "Deputy Mayor ") or starts-with(normalize-space(), "Councillor ")]'
        )
        assert len(headings) == 7, "Expected 7 council members"

        images = {image.get("alt"): image.get("src") for image in page.xpath("//img[@alt]")}
        seat_number = 1
        for heading in headings:
            title = heading.text_content().strip()
            if title.startswith("Mayor "):
                role = "Mayor"
                name = title[len("Mayor ") :]
                district = "Orangeville"
            elif title.startswith("Deputy Mayor "):
                role = "Deputy Mayor"
                name = title[len("Deputy Mayor ") :]
                district = "Orangeville"
            else:
                role = "Councillor"
                name = title[len("Councillor ") :]
                district = f"Orangeville (seat {seat_number})"
                seat_number += 1

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            for alt, src in images.items():
                if name in alt:
                    p.image = src
                    break
            yield p

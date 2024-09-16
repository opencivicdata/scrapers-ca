import re
from collections import defaultdict

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "http://www.woolwich.ca/en/council/council.asp"


class WoolwichPersonScraper(CanadianScraper):
    def scrape(self):
        seat_numbers = defaultdict(int)
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//td[@data-name="accParent"]/h2')
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            role, name = re.split(r"\s", councillor.text_content(), maxsplit=1)
            area = re.search(r"Ward \d", name)
            if not area:
                district = "Woolwich"
            else:
                seat_numbers[area] += 1
                district = area.group(0) + f" (seat {seat_numbers[area]})"
            if "(" in name:
                name = name.split(" (")[0]
            info = councillor.xpath("./ancestor::tr[1]/following-sibling::tr")[0].text_content()
            office = re.search(r"(?<=Office: )\d{3}-\d{3}-\d{4}", info).group(0)
            voice = (
                re.search(r"(?<=Toll Free: )(1-)?\d{3}-\d{3}-\d{4}( extension \d{4})?", info)
                .group(0)
                .replace("extension", "x")
            )

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_contact("voice", office, "office")
            p.add_contact("voice", voice, "legislature")

            yield p
